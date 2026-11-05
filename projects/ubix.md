A few corrupted slices can undermine an otherwise useful OCT scan. If an AI model gives those slices too much influence, its prediction for the whole volume can become unreliable. In our [Medical Image Analysis paper](https://doi.org/10.1016/j.media.2024.103259), we introduced **Uncertainty-Based Instance eXclusion (UBIX)** to address this problem.

### Let uncertainty guide the contribution of each slice

UBIX works with multiple-instance learning: individual slices contribute to a prediction for an entire volume. Before those contributions are pooled, UBIX uses uncertainty estimates to identify suspicious instances and reduce or exclude their influence.

The adjustment happens at inference time. The model does not need to be retrained on the new artifacts. Although we studied OCT slices, the same idea can be applied to other definitions of instances and bags.

### Testing beyond the training scanner

We evaluated UBIX for staging age-related macular degeneration. Models were trained using scans from one scanner and tested on external datasets from other vendors, including vendor-specific artifacts.

With UBIX, quadratic weighted kappa decreased from **0.861 to 0.708** on the external data containing artifacts. A state-of-the-art 3D network without UBIX decreased from **0.852 to 0.084** on the same test set. These are results for the evaluated models and datasets: they show how limiting the contribution of unfamiliar artifacts can help preserve performance across scanners.

### Code and publication

The [source code and trained model weights](https://github.com/qurAI-amsterdam/ubix-for-reliable-classification) are available on GitHub. The paper was published online on **27 June 2024** and appeared in the October 2024 issue of *Medical Image Analysis*. UBIX also features in my [PhD thesis](project-phd-thesis.html).
