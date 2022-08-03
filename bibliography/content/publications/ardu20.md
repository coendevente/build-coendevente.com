title: Artificial Intelligence for the Classification and Quantification of Reticular Pseudodrusen in Multimodal Retinal Images
authors: A. Ardu, B. Liefers, C. de Vente, C. González-Gonzalo, C. Klaver and C. Sánchez
has_pdf: False 
bibkey: ardu20
groups: diag
booktitle: European Society of Retina Specialists
year: 2020
doi: NA 
template: publication
diag_authors: coen-de-vente
journal: NA 


Purpose:

Reticular pseudodrusen (RPD) are retinal lesions highly correlated with the risk of developing end-stage age-related macular degeneration (AMD) and, therefore, relevant biomarkers for understanding the progression of AMD. Due to the subtle features characterizing RPD, multiple imaging modalities are often necessary to confirm the presence and extension of RPD, considerably increasing the workload of the expert graders. We propose a deep neural network (DNN) architecture that classifies and quantifies RPD using multimodal retinal images.

Setting:

A cross-sectional study that compares the performance of three expert graders with a DNN trained for identifying and quantifying RPD. Conducted on retinal images drawn from the Rotterdam Study, a population-based cohort, in three modalities: color fundus photographs (CFP), fundus autofluorescence images (FAF) and near-infrared reflectance images (NIR).

Methods:

Multimodal images of 278 eyes of 230 patients were retrieved from the Rotterdam Study database. Of those, 72 eyes showed presence of RPD, 108 had soft distinct/indistinct drusen, and 98 had no signs of drusen as confirmed by the Rotterdam Study graders. Delineations of the areas affected with RPD were made in consensus by two human experts using CFP and NIR images simultaneously and were used as reference standard (RS) for RPD area quantification. The data was randomly divided, patient-wise, in training (243) and test (35) sets for model development and evaluation. A DNN was developed for RPD classification and quantification. The proposed DNN is based on an encoder-decoder architecture. The model jointly inputs a set of co-registered retinal image modalities (CFP, NIR, FAF) and outputs a heatmap image containing, per pixel, the likelihood of RPD presence. The 99th percentile of the values contained in this heatmap measures the likelihood of RPD presence. Three independent graders manually delineated RPD in all eyes of the test set based on the CFP and NIR and their performance was compared with the DNN in the tasks of RPD classification and quantification.

Results:

The proposed DNN obtained an area under the receiver operating characteristic curve (AUROC) with 95% confidence interval (CI) of 0.939[0.818-1.0], a sensitivity (SE) of 0.928 and specificity (SP) of 0.809 for the detection of RPD in multimodal imaging. For RPD quantification, the DNN achieved a mean Dice coefficient (DSC) of 0.632+-0.261 and an intra-class correlation (ICC) of 0.676[0.294-0.999]. Comparably, for RPD classification, grader 1 obtained SE/SP pairs of 1.0/0.785, grader 2 of 1.0/0.5 and grader 3 of 1.0/0.785. For RPD quantification, the graders obtained mean DSC of 0.619+-0.196, 0.573+-0.170 and 0.697+-0.157, respectively, and an ICC of 0.721[0.340-0.999], 0.597[0.288-0.999], 0.751[0.294-0.999], respectively. Of the DNN's three false negatives, none of them was correctly classified by the three graders. The model correctly classified RPD in three of the six eyes where graders disagreed and in the only eye where none of the graders found RPD. Overall, 65.1% of the area indicated as RPD by the reference was delineated by at least one grader and only 26.5% of the total was graded as RPD by all experts. The DNN only missed 23.2% of the areas that all three graders identified correctly.

Conclusions:

The proposed DNN showed promising capacities in the tasks of classifying and quantifying RPD lesions on multimodal retinal images. The results show that the model is able to correctly classify and quantify RPD on eyes where lesions are difficult to spot. The probabilistic output of the model allows for the classification of RPD at different levels of confidence and indicates what retinal areas are most likely affected. This is in line with the manual assessment done by the graders. To this point, the model is developed to classify and quantify RPD only on CFP, FAF and NIR. However, introducing other imaging modalities, such as OCT, might help diminish ambiguities in the classification and quantification of this abnormality. Therefore, a future direction for improving the proposed method is to include OCT scans as an additional input to the model. Automatic classification and quantification of RPD using deep learning on multimodal images will enable the automatic and accurate analysis of increasingly large amounts of data for clinical studies and will facilitate AMD screening in the elderly  by decreasing the workload of the expert graders.

Financial Disclosure:

None

