### Purpose
Deep neural networks (DNNs) for optical coherence tomography (OCT) classification have been proven to work well on images from scanners that were used during training. However, since the appearance of OCT scans can differ greatly between vendors, these DNNs often fail when they are applied to scans from different manufacturers. We propose a DNN architecture for age-related macular degeneration (AMD) grading that maintains performance on OCTs from vendors not included during training.

### Methods
2,598 and 680 Heidelberg Spectralis OCT scans from the European Genetic Database were used for development and testing, respectively. We tested transferability with 339 AMD-enriched Topcon OCTs from the Rotterdam Study.

AMD severity classification was determined manually in accordance with the Cologne Image Reading Center and Laboratory and Rotterdam Classification, respectively. Classifications were harmonized for the evaluation of the DNNs.

The proposed DNN considers each B-scan separately using a 2D ResNet-18, and internally combines the intermediate outputs related to each B-scan using a multiple instance learning approach. Even though the proposed DNN provides both B-scan level and OCT-volume level decisions, the architecture is trained end-to-end using only full volume gradings. This specific architecture makes our method robust to the variability of scanning protocols across vendors, as it is invariant to B-scan spacing.

We compare this approach to a baseline that classifies the full OCT scan directly using a 3D ResNet-18.

### Results
The quadratic weighted kappa (QWK) for the baseline method dropped from 0.852 on the Heidelberg Spectralis dataset to 0.523 on the Topcon dataset. This QWK drop was smaller (p = 0.001) for our approach, which dropped from 0.849 to 0.717. The difference in area under the Receiver Operating Characteristic (AUC) drop was also smaller (p < 0.001) for our approach (0.969 to 0.906, -6.5%) than for the baseline method (0.971 to 0.806, -17.0%).

### Conclusions
We present a DNN for AMD classification on OCT scans that transfers well to scans from vendors that were not used for development. This alleviates the need for retraining on data from these scanner types, which is an expensive process in terms of data acquisition, model development, and human annotation time. Furthermore, this increases the applicability of AI for OCT classification in broader scopes than the settings in which they were developed.