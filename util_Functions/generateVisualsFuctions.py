from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw # to generate pdf report
import pubchempy as pcp
import os
from reportlab.lib.pagesizes import letter # report lab used to generate pdf report
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


from util_Functions.generalFunctions import defang_datetime, createFolderIfNotExists, sanitize_filename


# generate molecule name -- OLD not used
def get_molecule_name(smiles):
    compound = pcp.get_compounds(smiles, 'smiles')
    if compound:
        return compound[0].synonyms[0] if compound[0].synonyms else "Unknown"
    return "Unknown"


# generate 3d model
def use_rdkit_gen_3d_model(smiles):
    # Convert SMILES to 3D structure
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, AllChem.ETKDG())

    # Generate 3D coordinates (MolBlock)
    mol_block = Chem.MolToMolBlock(mol)
    return mol_block


# Save visual of molecule
def save_html_output(molecule_name, mol_block, output_Folder_Name):
    # Create minimal HTML content with the molecule name and model viewer
    minimal_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{molecule_name} - 3D Model</title>
        <script src="https://3dmol.csb.pitt.edu/build/3Dmol-min.js"></script>
    </head>
    <body>
        <div style="text-align: center;">
            <h1>{molecule_name}</h1>
            <div id="model-container" style="width: 600px; height: 400px; margin: 0 auto;"></div>
        </div>
        <script>
            const molBlock = `{mol_block}`;
            const viewer = $3Dmol.createViewer("model-container", {{ backgroundColor: "white" }});
            viewer.addModel(molBlock, "mol");
            viewer.setStyle({{}}, {{stick: {{}}}});
            viewer.zoomTo();
            viewer.render();
        </script>
    </body>
    </html>
    """
    
    createFolderIfNotExists(output_Folder_Name)
    output_file = os.path.join(output_Folder_Name, molecule_name)
    
    # Write the minimal HTML to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(minimal_html)
    
    print(f"Molecule 3D output saved to: {output_file}")


# generate pdb file
def generate_pdb(smiles, output_file, output_Folder_Name):
    # Convert SMILES to a molecule object
    mol = Chem.MolFromSmiles(smiles)
    
    if mol is None:
        print("Invalid SMILES string.")
        return

    # Generate 3D coordinates
    AllChem.EmbedMolecule(mol)
    AllChem.UFFOptimizeMolecule(mol)

    createFolderIfNotExists(output_Folder_Name)
    output_file = os.path.join(output_Folder_Name, output_file)

    # Write to PDB file
    with open(output_file, 'w') as f:
        f.write(Chem.MolToPDBBlock(mol))


# generate PDF report of all info seen
def generate_pdf_report(smiles, chemical_properties, output_folder):

    createFolderIfNotExists(output_folder)# Create a directory to store images
    
    # Generate the molecule from SMILES
    molecule = Chem.MolFromSmiles(smiles)
    
    if molecule is None:
        raise ValueError("Invalid SMILES string.")
    
    # Create a 2D image of the molecule
    img_path = os.path.join(output_folder, 'molecule_name_for_pdf_report.png')
    img = Draw.MolToImage(molecule, size=(300, 300))
    img.save(img_path)
    
    # Create a PDF report
    pdf_path = os.path.join(output_folder,f'{chemical_properties["Title"]}_report.pdf')
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Draw the title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 720, "Molecule Data Report")
    
    # Draw the molecule image
    c.drawImage(img_path, 72, 400, width=3 * inch, height=3 * inch)
    
    # Draw the molecular information
    c.setFont("Helvetica", 12)
    for i, (key, value) in enumerate(chemical_properties.items()):
        c.drawString(72, 350 - i * 20, f"{key}: {value}")
    
    # Finish the PDF
    c.showPage()
    c.save()
    
    print(f"PDF report generated: {pdf_path}")
