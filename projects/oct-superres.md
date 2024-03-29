### Purpose
In optical coherence tomography scans (OCTs) from multicenter studies, there is often large variability in image quality and resolution between scans. This impairs the consistency of biomarker quantification within studies, but also between different datasets. The aim of this study was to validate a super-resolution approach based on artificial intelligence (AI) for improving the resolution of OCTs (by increasing the density of the scan pattern) to consistently enhance data within studies to high-quality standards. 

### Methods
The MACUSTAR cohort, a European multicentre study, was used as a training set with 743 OCTs from 181 patients and validation set with 26 OCTs from 26 patients (n=3 no AMD, n=2 early AMD, n=18 intermediate AMD, n=3 late AMD). All scans were Heidelberg Spectralis OCTs with 241 B-scans. We trained a [3D diffusion model](https://arxiv.org/abs/2204.03458) to generate high-resolution OCTs, which was used during evaluation to produce OCTs with 241 B-scans from OCTs with 120 B-scans using [RePaint](https://arxiv.org/abs/2201.09865) [1]. The performance was calculated using the mean squared error (MSE) on OCT volume-level between the generated B-scans and the original B-scans.

<!-- <img src="images/oct-superres/inpainting.png" width=400/ style="margin-left: calc(50% - 200px); max-width: 100%;" alt="Inpainting example, showing every other B-scan is interpolated."> -->

<br>
<figure>
  <img src="images/oct-superres/superres_methods_overview.png" style="width: 100%;" alt="Methods overview.">
  <figcaption>
  Methods overview.
</figcaption>
</figure>

### Results
The MSE between the generated B-scans from the low-resolution OCTs and the original B-scans from the high-resolution OCTs was 0.006 ± 0.004 (mean ± SD). The figure below shows visual examples of the generated OCTs compared to the original B-scans in the validation set.

<figure>
  <img src="images/oct-superres/results_fig.jpg" width="100%" style="" alt="Results example figure.">
  <figcaption>Qualitative examples of generated OCTs compared to original OCTs, along with OCT-level MSEs. In each example, the top row shows the original OCTs and the bottom row shows the generated OCTs. The first column shows the en face projection of the OCT scan, obtained by averaging all A-scans. Black and white lines next to each B-scan in the en face indicate whether that B-scan was generated or present in the low-resolution OCT, respectively. The last three columns show the B-scans of which the positions in the OCT volume are indicated in red in the en face projection.
</figcaption>
</figure>

### Conclusions
We showed the feasibility of the proposed approach to generate super-resolution OCTs, which is one of the required steps to standardize high-quality OCTs within multicenter studies. In extensions of this approach, coherence between the OCT and other modalities, such as en face imaging and other metadata, could be introduced, allowing the AI model to make better informed generative decisions.

### Disclaimers
The communication reflects the authors' views. Neither IMI nor the European Union, EFPIA, or any associated partners are responsible for any use that may be made of the information contained therein.

The header image of the so-called "OCT jungle" was generated by [DALL·E 2](https://openai.com/product/dall-e-2).

### References
1. Lugmayr, A., Danelljan, M., Romero, A., Yu, F., Timofte, R., & Van Gool, L. (2022). Repaint: Inpainting using denoising diffusion probabilistic models. In <i>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition</i> (pp. 11461-11471).
