OCT scans can reveal early signs of retinal atrophy, but differences between scanners make automated assessment difficult. In our [MACUSTAR paper](https://doi.org/10.1167/tvst.13.9.11), we developed a model to detect **incomplete and complete retinal pigment epithelium and outer retinal atrophy (iRORA and cRORA)** across devices.

### From individual features to atrophy

The pipeline combines domain adaptation with segmentation. It first reduces differences in image appearance, then detects the granular biomarkers used to identify iRORA and cRORA. These predictions are combined into atrophy segmentations.

### Evaluation in MACUSTAR

We compared the algorithm with manual annotations in **168 patients with intermediate age-related macular degeneration**. For the three-way distinction between no atrophy, iRORA and cRORA, quadratic weighted kappa was **0.73 on Spectralis** and **0.37 on ZEISS** scans. Removing domain adaptation reduced the Spectralis score to 0.63.

It forms part of my [PhD thesis](project-phd-thesis.html) on robust medical imaging AI.
