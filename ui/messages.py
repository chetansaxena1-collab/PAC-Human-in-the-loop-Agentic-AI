"""
UI messages used throughout the PAC application.
"""

import streamlit as st


def show_regulatory_guidance():
    """
    Display guidance when no regulatory match is found.
    """

    st.info(
        """
### ℹ️ PAC AI Guidance

PAC AI searches and matches regulatory terminology exactly as defined in the applicable regulatory guideline.

To obtain the most accurate recommendation, please describe your proposed change using **complete regulatory terminology or phrases** rather than short keywords or informal descriptions.

---

### ✅ Examples of preferred regulatory terminology

- Addition of a manufacturing site
- Addition or replacement of a batch release site
- Deletion of a supplier of starting material

---

### ⚠ Examples of phrases that may not produce an accurate match

- Site addition
- New site
- Change site

These phrases may not uniquely identify the appropriate regulatory pathway.

---

### 📖 Recommendation

Please refer to the applicable regulatory guideline, revise your request using complete regulatory terminology, and try again.
"""
    )

    with st.expander("📖 View Sample Regulatory Phrases"):

        st.markdown(
            """
### Manufacturing Site Changes

- Addition of a manufacturing site
- Addition or replacement of a manufacturing site
- Deletion of a manufacturing site

### Batch Release Site Changes

- Addition or replacement of a batch release site
- Change in batch release site

### Testing Site Changes

- Addition of a testing site
- Addition or replacement of a quality control site

### Supplier Changes

- Addition of a supplier of starting material
- Deletion of a supplier
- Change in supplier of active substance

### Manufacturing Process Changes

- Change in manufacturing process
- Change in manufacturing procedure
- Change in manufacturing equipment
"""
        )