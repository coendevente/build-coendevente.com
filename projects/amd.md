### Abstract

#### Purpose
Deep convolutional neural networks (CNNs) are increasingly being used for eye disease screening and diagnosis. Especially the best performing variants, however, are generally overconfident in their predictions. For usefulness in clinical practice and increasing clinicians’ trust on the estimated diagnosis, well-calibrated uncertainty estimates are necessary. We present a method for providing confidence scores of CNNs for age-related macular degeneration (AMD) grading in optical coherence tomography (OCT).

#### Methods
1,264 OCT volumes from 633 patients from the European Genetic Database (EUGENDA) were graded as one of five stages of AMD (No AMD, Early AMD, Intermediate AMD, Advanced AMD: GA, and Advanced AMD: CNV). Ten different 3D DenseNet-121 models that take a full OCT volume as input were used to predict the corresponding AMD stage. These networks were all trained on the same dataset. However, each of these networks were initialized differently. The class with the maximum average softmax output of these models was used as the final prediction. The confidence measure was the normalized average softmax output for that class.

#### Results
The algorithm achieved an area under the Receiver Operating Characteristic of 0.9785 and a quadratic-weighted kappa score of 0.8935. The mean uncertainty, calculated as 1 - the mean confidence score, for incorrect predictions was 1.9 times as high as the mean uncertainty for correct predictions. When only using the probability output of a single network, this ratio was 1.4. Another measure for uncertainty estimation performance is the Expected Calibration Error (ECE), where a lower value is better. When comparing the method to the probability output of a single network, the ECE improved from 0.0971 to 0.0324. Figure 1 shows examples of both confident and unconfident predictions.

#### Conclusions
We present a method for improving uncertainty estimation for AMD grading in OCT, by combining the output of multiple individually trained CNNs. This increased reliability of system confidences can contribute to building trust in CNNs for retinal disease screening. Furthermore, this technique is a first step towards selective prediction in retinal disease screening, where only cases with high uncertainty predictions need to be referred for expert evaluation.

<img src="images/amd1.png" style="width: 100%;" />

### ARVO Presentation
<div class="video-container">
    <iframe width="100%" src="https://www.youtube.com/embed/Bokh6sU63rg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
