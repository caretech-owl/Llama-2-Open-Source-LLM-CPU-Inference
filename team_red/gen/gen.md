# Project Protocol Gen

## To do

### 1. [x] **Enhance Model output**:  

Loading the model directly instead of through the transformers pipeline not only enhances the general output but decreases model run time for cpu inference as well.

### 2. [ ] **Rephrase single sentences, allow continous writing**:  

Gradio only supports interactivity between user and application to a certain degree. The HightlightedText Component can only be used to assign labels to certain phrases and or sentences and is often used in sentiment analysis or to show confidence scores. User input through this module e.g. selecting a text snippet and retrieving that said snippet is not possible.\
As a result, the current code only supports adding notes to the already generated text to continue to grow the document. So rephrasing is not yet supported as it was meant. When adding additional text to the generated text, everything needs to be put into the model again for the model to remember. First tests show that putting only the newly added sentences into the model generates contextual gibberish.

When prompting with additional text ***only*** e.g.:\
*"OP am 3.1.2024, Entlassung danach am 10. Januar."*

The model outputs:\
*"Patientname: Jane Smith, Aufnahme: 01-03-2024, Entlassung: 01-10-2024"*

But if the additional text is passed into the model together with the already generated text, the model acknowledges the already established form/layout of the previous texts' sentences and simply adds these lines to it.

When prompting with additional text ***and*** previously generated text e.g.:\
generated_text + *"OP am 3.1.2024, Entlassung danach am 10. Januar."*

The model outputs:\
rephrased_generated_text + *"Eine Operation ist für den 3. Januar 2024 geplant und der Patient wird am 10. Januar entlassen."*




**PARAMETER AND ADDITIONAL DOCUMENTATION WORK IN PROGRESS!**
