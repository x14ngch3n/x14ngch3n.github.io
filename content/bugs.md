---
title: "Bugs"
---

## OSS bugs

- [unace: heap buffer over-read in magic scanner](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1138160)
- [unace-nonfree: overlapping strcpy in path processing](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1138161)
- [llama.cpp: ggml-backend-meta axis <= GGML_MAX_DIMS off-by-one](https://github.com/ggml-org/llama.cpp/issues/26367)
- [mlx: out-of-bounds read in GGUF metadata loader](https://github.com/ml-explore/mlx/issues/4213) ([fix](https://github.com/ml-explore/mlx/pull/4212))
- [llama.cpp: GGUF loader accepts a tensor size that wraps to 0 after padding](https://github.com/ggml-org/llama.cpp/issues/26978)
- [LiteRT: integer overflow to out-of-bounds](https://github.com/google-ai-edge/LiteRT/issues/9255)
- [stable-diffusion.cpp: signed shape-product wrap in safetensors reader](https://github.com/leejet/stable-diffusion.cpp/issues/1876)

## CVEs

- [CVE-2021-XXXX command injection in XXX IoT device](https://nvd.nist.gov/vuln/detail/CVE-2021-XXXX)
