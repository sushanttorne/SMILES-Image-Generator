import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw
from io import BytesIO

st.title("SMILES to Image Converter")
st.write(
    "This app takes a **SMILES** string as input and generates the corresponding molecular structure image. "
    "For example, try 'CCO' (Ethanol) or 'C1=CC=CC=C1' (Benzene)."
)

# Initialize session state for smiles input
if "smiles_input" not in st.session_state:
    st.session_state.smiles_input = ""

# Example button — sets session state BEFORE the text_input renders
if st.button("Try Example (Benzene)"):
    st.session_state.smiles_input = "C1=CC=CC=C1"

# Text input bound to session state
smiles = st.text_input("Enter SMILES string:", value=st.session_state.smiles_input)

# Validate and process input
if smiles.strip():
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            img = Draw.MolToImage(mol, size=(400, 400))

            img_buffer = BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            st.image(img, caption=f"Structure for: {smiles}")

            st.download_button(
                label="Download Molecule Image as PNG",
                data=img_buffer,
                file_name="molecule.png",
                mime="image/png"
            )
        else:
            st.error("Invalid SMILES string. Please check your input and try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Enter a SMILES string above to generate the molecular structure.")
