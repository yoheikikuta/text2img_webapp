import numpy as np
import torch as th
from glide_text2im.download import load_checkpoint
from glide_text2im.model_creation import (
    create_model_and_diffusion,
    model_and_diffusion_defaults,
    model_and_diffusion_defaults_upsampler
)


class Text2ImgML:
    def __init__(self) -> None:
        has_cuda = th.cuda.is_available()
        self.device = th.device('cpu' if not has_cuda else 'cuda')

        # model: text to 64x64 image
        self.options = model_and_diffusion_defaults()
        self.options['use_fp16'] = has_cuda
        self.options['timestep_respacing'] = '20' # use 100 diffusion steps for fast sampling
        self.model, self.diffusion = create_model_and_diffusion(**self.options)
        self.model.eval()
        if has_cuda:
            self.model.convert_to_fp16()
        self.model.to(self.device)

        # model_up: 64x64 to 256x256
        self.options_up = model_and_diffusion_defaults_upsampler()
        self.options_up['use_fp16'] = has_cuda
        self.options_up['timestep_respacing'] = 'fast27' # use 27 diffusion steps for very fast sampling
        self.model_up, self.diffusion_up = create_model_and_diffusion(**self.options_up)
        self.model_up.eval()
        if has_cuda:
            self.model_up.convert_to_fp16()
        self.model_up.to(self.device)

    def load(self) -> None:
        """
        When server is activated, load model weight.
        """
        self.model.load_state_dict(th.load('/model/model.pt', map_location=self.device))
        self.model_up.load_state_dict(th.load('/model/model_up.pt', map_location=self.device))

    def predict(self, text:str) -> np.ndarray:
        """
        """
        batch_size = 5
        upsample_temp = 0.997

        tokens = self.model.tokenizer.encode(text)
        tokens, mask = self.model.tokenizer.padded_tokens_and_mask(tokens, self.options['text_ctx'])

        # Create the classifier-free guidance tokens (empty)
        full_batch_size = batch_size * 2
        uncond_tokens, uncond_mask = self.model.tokenizer.padded_tokens_and_mask([], self.options['text_ctx'])

        # Pack the tokens together into model kwargs.
        model_kwargs = dict(
            tokens=th.tensor([tokens] * batch_size + [uncond_tokens] * batch_size, device=self.device),
            mask=th.tensor([mask] * batch_size + [uncond_mask] * batch_size, dtype=th.bool, device=self.device,),
        )

        self.model.del_cache()
        samples = self.diffusion.p_sample_loop(
            self._model_fn,
            (full_batch_size, 3, self.options["image_size"], self.options["image_size"]),
            device=self.device,
            clip_denoised=True,
            progress=True,
            model_kwargs=model_kwargs,
            cond_fn=None,
        )[:batch_size]
        self.model.del_cache()

        # TODO: add upsampling step.
        return self._convert_result_tensor_to_ndarray(samples)

    def _model_fn(self, x_t, ts, **kwargs):
        guidance_scale = 3.0

        half = x_t[: len(x_t) // 2]
        combined = th.cat([half, half], dim=0)
        model_out = self.model(combined, ts, **kwargs)
        eps, rest = model_out[:, :3], model_out[:, 3:]
        cond_eps, uncond_eps = th.split(eps, len(eps) // 2, dim=0)
        half_eps = uncond_eps + guidance_scale * (cond_eps - uncond_eps)
        eps = th.cat([half_eps, half_eps], dim=0)

        return th.cat([eps, rest], dim=1)

    def _convert_result_tensor_to_ndarray(self, samples: th.Tensor) -> np.ndarray:
        scaled = ((samples + 1)*127.5).round().clamp(0,255).to(th.uint8).cpu()
        reshaped = scaled.permute(2, 0, 3, 1).reshape([samples.shape[2], -1, 3])

        return reshaped.numpy()