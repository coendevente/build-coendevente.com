title: Hierarchical curriculum learning for robust automated detection of low-prevalence retinal disease features: application to reticular pseudodrusen
authors: C. González-Gonzalo, E. Thee, B. Liefers, C. de Vente, C. Klaver and C. Sánchez
has_pdf: False 
bibkey: gonz21
groups: diag
booktitle: Association for Research in Vision and Ophthalmology
year: 2021
doi: NA 
template: publication
diag_authors: coen-de-vente
journal: NA 


Purpose: The low prevalence of certain retinal disease features compromises data collection for deep neural networks (DNN) development and, consequently, the benefits of automated detection. We robustify the detection of such features in scarce data settings by exploiting hierarchical information available in the data to learn from generic to specific, low-prevalence features. We focus on reticular pseudodrusen (RPD), a hallmark of intermediate age-related macular degeneration (AMD).

Methods: Color fundus images (CFI) from the AREDS dataset were used for DNN development (106,994 CFI) and testing (27,066 CFI). An external test set (RS1-6) was generated with 2,790 CFI from the Rotterdam Study. In both datasets CFI were graded from generic to specific features. This allows to establish a hierarchy of binary classification tasks with decreasing prevalence: presence of AMD findings (AREDS prevalence: 88%; RS1-6: 77%), drusen (85%; 73%), large drusen (40%; 24%), RPD (1%; 4%). We created a hierarchical curriculum and developed a DNN (HC-DNN) that learned each task sequentially. We computed its performance for RPD detection in both test sets and compared it to a baseline DNN (B-DNN) that learned to detect RPD from scratch disregarding hierarchical information. We studied their robustness across datasets, while reducing the size of data available for development (same prevalences)

Results: Area under the receiver operating characteristic curve (AUC) was used to measure RPD detection performance. When large development data were available, there was no significant difference between DNNs (100% data, HC-DNN: 0.96 (95% CI, 0.94-0.97) in AREDS, 0.82 (0.78-0.86) in RS1-6; B-DNN: 0.95 (0.94-0.96) in AREDS, 0.83 (0.79-0.87) in RS1-6). However, HC-DNN achieved better performance and robustness across datasets when development data were highly reduced (<50% data, p-values<0.05) (1% data, HC-DNN: 0.63 (0.60-0.66) in AREDS, 0.76 (0.72-0.80) in RS1-6; B-DNN: 0.53 (0.49-0.56) in AREDS, 0.48 (0.42-0.53) in RS1-6).

Conclusions: Hierarchical curriculum learning allows for knowledge transfer from general, higher-prevalence features and becomes beneficial for the detection of low-prevalence retinal features, such as RPD, in scarce data settings. Moreover, exploiting hierarchical information improves DNN robustness across datasets.

