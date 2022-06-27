#!/usr/bin/sh
if [ ! -e "/etc/systemd/system/text2img.service" ]; then
	{
		echo "[Unit]"
		echo "Description=text2img backend server"
		echo "Requires=docker.service"
		echo "After=docker.service"
		echo ""
		echo "[Service]"
		echo "Restart=always"
		echo "TimeoutStartSec=2min"
		echo "RestartSec=2min"
		echo "ExecStart=/usr/bin/docker start -a backend"
		echo "ExecStop=/usr/bin/docker stop backend"
		echo ""
		echo "[Install]"
		echo "WantedBy=default.target"
	} >> /etc/systemd/system/text2img.service

	docker pull GCR_IMAGE
	docker run -d --gpus all --name backend -p 80:80 GCR_IMAGE
	docker stop backend
	systemctl daemon-reload
	systemctl start text2img
	systemctl enable text2img
fi