import pubchempy as pcp
import requests 

def get_chemical_properties(smiles):
# def get_chemical_properties(smiles='CC1=C(C=C(C=C1[N+](=O)[O-])[N+](=O)[O-])[N+](=O)[O-]'):
    # API endpoint to get all chemical properties from PubChem using SMILES
    # FULL DATA AVAILABLE:
    # url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES,InChI,InChIKey,IUPACName,Title,XLogP,ExactMass,MonoisotopicMass,TPSA,Complexity,Charge,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,IsotopeAtomCount,AtomStereoCount,DefinedAtomStereoCount,UndefinedAtomStereoCount,BondStereoCount,DefinedBondStereoCount,UndefinedBondStereoCount,CovalentUnitCount,PatentCount,PatentFamilyCount,LiteratureCount,Volume3D,XStericQuadrupole3D,YStericQuadrupole3D,ZStericQuadrupole3D,FeatureCount3D,FeatureAcceptorCount3D,FeatureDonorCount3D,FeatureAnionCount3D,FeatureCationCount3D,FeatureRingCount3D,FeatureHydrophobeCount3D,ConformerModelRMSD3D,EffectiveRotorCount3D,ConformerCount3D,Fingerprint2D/JSON'
    
    
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/property/MolecularFormula,MolecularWeight,IUPACName,Title,ExactMass,MonoisotopicMass,IsotopeAtomCount,Charge,TPSA,XLogP,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,HeavyAtomCount,Volume3D,Complexity,Fingerprint2D/JSON'

    
    # Make the request
    response = requests.get(url)
    
    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        
        # Extract properties
        properties = data['PropertyTable']['Properties'][0]
        return {
            'SMILES': smiles,
            'Molecular Formula': properties.get('MolecularFormula', 'N/A'),
            'Molecular Weight': properties.get('MolecularWeight', 'N/A'),
            'IUPAC Name': properties.get('IUPACName', 'N/A'),
            'Title': properties.get('Title', 'N/A'),
            'Exact Mass': properties.get('ExactMass', 'N/A'),
            'Monoisotopic Mass': properties.get('MonoisotopicMass', 'N/A'),
            'Isotope Atom Count': properties.get('IsotopeAtomCount', 'N/A'),
            'Charge': properties.get('Charge', 'N/A'),
            'Topological Polar Surface Area': properties.get('TPSA', 'N/A'),
            'XLogP': properties.get('XLogP', 'N/A'),
            'HBond Donor Count': properties.get('HBondDonorCount', 'N/A'),
            'HBond Acceptor Count': properties.get('HBondAcceptorCount', 'N/A'),
            'Rotatable Bond Count': properties.get('RotatableBondCount', 'N/A'),
            'Heavy Atom Count': properties.get('HeavyAtomCount', 'N/A'),
            'Volume3D': properties.get('Volume3D', 'N/A'),
            'Complexity': properties.get('Complexity', 'N/A'),
            'Fingerprint2D': properties.get('Fingerprint2D', 'N/A')
        }
    else:
        print(f"Error fetching data for SMILES: {smiles}")
        print(f"response code: {response.status_code}")
        return None