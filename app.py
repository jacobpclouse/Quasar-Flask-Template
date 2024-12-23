from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_cors import CORS  # Import the CORS library

# Import other functions internally
from util_Functions.generalFunctions import myLogo, defang_datetime, createFolderIfNotExists, sanitize_filename, emptyFolder
from util_Functions.apiFunctions import get_chemical_properties
from util_Functions.generateVisualsFuctions import use_rdkit_gen_3d_model,  save_html_output, generate_pdb, generate_pdf_report   #, get_molecule_name

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
OUTPUT_FOLDER_NAME = 'OUTPUTS'  # folder where all the output files should be stored
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
@app.route('/api/generate', methods=['POST'])
def generate_molecule_api():
    # title = "Molecule Viewer - SMILES to 3D Model!"  # Default title
    createFolderIfNotExists(OUTPUT_FOLDER_NAME)
    emptyFolder(OUTPUT_FOLDER_NAME)

    data = request.json
    smiles = data.get('smiles')

    if not smiles:
        print("YOU NEED TO SUBMIT A SMILES STRING")
        return jsonify({'error': 'SMILES string is missing'}), 400
    else:
        print(f"Received SMILES: {smiles}")

    # Your logic to generate molecule properties
    all_molecule_properties = get_chemical_properties(smiles) # maybe have it return a dummy smiles if smiles formula isn't valid
    
    if all_molecule_properties == None:
        print("The Smiles you submitted was for an element that doesn't exist and wasn't understood")
        return jsonify({'error': 'SMILES string was Invalid check syntax'}), 400
    else:
        print(f"Molecule Name: {all_molecule_properties['Title']}")

    # you need to 
    # molecule_name = all_molecule_properties['Title'] # need to sep
    molecule_name_sanitized = sanitize_filename(all_molecule_properties['Title']) # this is used as filename so we dont have invalid characters

    mol_block = use_rdkit_gen_3d_model(smiles)

    # for downloads - add these to return later
    generate_pdb(smiles, f"{molecule_name_sanitized}__Data.pdb", OUTPUT_FOLDER_NAME)
    save_html_output(f"{molecule_name_sanitized}__Visual.html", mol_block, OUTPUT_FOLDER_NAME)
    generate_pdf_report(smiles, all_molecule_properties, OUTPUT_FOLDER_NAME)

    return jsonify({
        'molecule_name': all_molecule_properties['Title'],
        'mol_block': mol_block,
        # below will be the table data
        'mol_Molecular_Formula': all_molecule_properties['Molecular Formula'],
        'mol_Molecular_Weight': all_molecule_properties['Molecular Weight'],
        'mol_IUPAC_Name': all_molecule_properties['IUPAC Name'],
        'mol_Exact_Mass': all_molecule_properties['Exact Mass'],
        'mol_Monoisotopic_Mass': all_molecule_properties['Monoisotopic Mass'],
        'mol_Isotope_Atom_Count': all_molecule_properties['Isotope Atom Count'],
        'mol_Charge': all_molecule_properties['Charge'],
        'mol_Topological_Polar_Surface_Area': all_molecule_properties['Topological Polar Surface Area'],
        'mol_XLogP': all_molecule_properties['XLogP'],
        'mol_HBond_Donor_Count': all_molecule_properties['HBond Donor Count'],
        'mol_HBond_Acceptor_Count': all_molecule_properties['HBond Acceptor Count'],
        'mol_Rotatable_Bond_Count': all_molecule_properties['Rotatable Bond Count'],
        'mol_Heavy_Atom Count': all_molecule_properties['Heavy Atom Count'],
        'mol_Volume3D': all_molecule_properties['Volume3D'],
        'mol_Complexity': all_molecule_properties['Complexity'],
        'mol_Fingerprint2D': all_molecule_properties['Fingerprint2D']
    })


# Main Flask routine
# Route to generate molecule and render it in HTML -- used for bootstrap and orig was at '/', can we get rid of this?
@app.route('/indexOld', methods=['GET', 'POST'])
def index():
    title = "SMILES to 3D Model!"  # Default title
    myLogo()
    createFolderIfNotExists(OUTPUT_FOLDER_NAME)
    mol_block = ""
    molecule_name = ""
    molecule_name_sanitized = ""
    spectral_data= ""
    if request.method == 'POST':
        defang_datetime()
        smiles = request.form['smiles']
        print(f"Received SMILES: {smiles}")

        # can i replace below molecule name with results from api?
        all_molecule_properties = get_chemical_properties(smiles)

        # molecule_name = get_molecule_name(smiles) # OLD from pcp
        molecule_name = all_molecule_properties['Title']
        molecule_name_sanitized = sanitize_filename(molecule_name)
        print(f"Molecule Name: {molecule_name}")
        spectral_data = all_molecule_properties['Molecular Formula']


        mol_block = use_rdkit_gen_3d_model(smiles)
        # spectral_data = get_spectral_info(smiles, molecule_name_sanitized)
        generate_pdb(smiles, f"{molecule_name_sanitized}__Data.pdb", OUTPUT_FOLDER_NAME)
        save_html_output(f"{molecule_name_sanitized}__Visual.html", mol_block, OUTPUT_FOLDER_NAME)
    
    # return render_template('index.html', mol_block=mol_block, molecule_name=molecule_name)
    return render_template('index.html', title=title, mol_block=mol_block, molecule_name=molecule_name, pdb_filename=f"{molecule_name_sanitized}__Data.pdb",spectral_data=spectral_data)

# download pdb
@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory('OUTPUTS', filename, as_attachment=True)



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main -- debug mode setup below
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
if __name__ == '__main__':
    app.run(debug=True)

