<template>
  <q-layout view="lHh Lpr lFf" class="bg-white">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round @click="toggleLeftDrawer" aria-label="Menu" icon="menu" />
        <q-toolbar-title>Molecule Viewer</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="bg-grey-2">
      <q-list>
        <q-item-label header>Navigation</q-item-label>
        <q-item clickable @click="goToPage('/')">
          <q-item-section avatar>
            <q-icon name="science" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Molecule Viewer</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <q-page class="q-pa-md">
        <q-card class="q-pa-md">
          <q-card-section>
            <q-input
              v-model="smiles"
              label="Enter SMILES"
              filled
              type="search"
              hint="Search for Molecule Data using SMILES Formula"
            >
              <template v-slot:append>
                <q-icon name="search" color="primary" @click="generateMolecule" />
              </template>
            </q-input>
          </q-card-section>

          <q-card-section>
            <div v-if="molecularInfo.length === 0" class="q-pa-md flex flex-center">
              <q-icon name="science" size="100px" color="grey-5" />
              <div class="text-subtitle1 q-mt-md">
                Enter a SMILES formula to view molecule data!
              </div>
            </div>

            <q-splitter v-else v-model="splitModel" style="height: 100%">
              <template v-slot:before>
                <q-card-section v-if="molecularInfo.length > 0">
                  <q-card-section v-if="molecule_name">
                    <div class="text-h6">
                      Molecule Data:
                      <q-badge>{{ molecule_name }}</q-badge>
                    </div>
                  </q-card-section>
                  <q-table :rows="molecularInfo" :columns="columns" row-key="property" hide-header hide-bottom :rows-per-page-options="[0]" style="width: 100%; height: 100%" />
                </q-card-section>
              </template>

              <template v-slot:after>
                <div>
                  <div id="model-container" style="width: 100%; height: 600px;"></div>
                  <div class="flex justify-center">
                    <q-btn-group flat>
                      <q-btn outline label="Stick" @click="changeStyle('stick')" />
                      <q-btn outline label="Line" @click="changeStyle('line')" />
                      <q-btn outline label="Sphere" @click="changeStyle('sphere')" />
                      <q-btn outline label="Cross" @click="changeStyle('cross')" />
                      <q-btn color="secondary" label="Download PDB" @click="downloadPDB" />
                      <q-btn color="primary" label="Download PDF Report" @click="downloadChemReport" />
                    </q-btn-group>
                  </div>
                </div>
              </template>
            </q-splitter>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import axios from "axios";
import { ref, nextTick } from "vue";
import * as $3Dmol from "3dmol";

export default {
  name: "MyLayout",

  setup() {
    const leftDrawerOpen = ref(false);
    const smiles = ref("");
    const molecule_name = ref("");
    const mol_block = ref("");
    const molecularInfo = ref([]);
    const splitModel = ref(50);
    const viewer = ref(null);
    const columns = [
      { name: "property", align: "left", label: "Property", field: "property" },
      { name: "value", align: "left", label: "Value", field: "value" },
    ];

    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value;
    };

    const generateMolecule = async () => {
      try {
        molecularInfo.value = [];
        molecule_name.value = "";

        const response = await axios.post(
          "http://127.0.0.1:5000/api/generate",
          { smiles: smiles.value }
        );

        molecule_name.value = response.data.molecule_name;
        mol_block.value = response.data.mol_block;

        molecularInfo.value = [
          { property: "Molecular Formula", value: response.data.mol_Molecular_Formula },
          { property: "Molecular Weight", value: response.data.mol_Molecular_Weight },
          { property: "IUPAC Name", value: response.data.mol_IUPAC_Name },
          { property: "Exact Mass", value: response.data.mol_Exact_Mass },
          { property: "Monoisotopic Mass", value: response.data.mol_Monoisotopic_Mass },
          { property: "Isotope Atom Count", value: response.data.mol_Isotope_Atom_Count },
          { property: "Charge", value: response.data.mol_Charge },
          { property: "Topological Polar Surface Area", value: response.data.mol_Topological_Polar_Surface_Area },
          { property: "XLogP", value: response.data.mol_XLogP },
          { property: "HBond Donor Count", value: response.data.mol_HBond_Donor_Count },
          { property: "HBond Acceptor Count", value: response.data.mol_HBond_Acceptor_Count },
          { property: "Rotatable Bond Count", value: response.data.mol_Rotatable_Bond_Count },
          { property: "Heavy Atom Count", value: response.data.mol_Heavy_Atom_Count },
          { property: "Volume3D", value: response.data.mol_Volume3D },
          { property: "Complexity", value: response.data.mol_Complexity },
          { property: "Fingerprint2D", value: response.data.mol_Fingerprint2D },
        ];

        await nextTick();
        renderMolecule();
      } catch (error) {
        console.error("Error generating molecule:", error);
      }
    };

    const renderMolecule = () => {
      if (mol_block.value) {
        viewer.value = $3Dmol.createViewer("model-container", {
          backgroundColor: "white",
        });
        viewer.value.addModel(mol_block.value, "mol");
        viewer.value.setStyle({}, { stick: {} }); // Default to Stick style
        viewer.value.zoomTo();
        viewer.value.render();
      }
    };

    const changeStyle = (styleType) => {
      // Clear the current styles
      viewer.value.setStyle({}, null);

      // Apply the selected style
      if (styleType === 'stick') {
        viewer.value.setStyle({}, { stick: {} });
      } else if (styleType === 'line') {
        viewer.value.setStyle({}, { line: {} });
      } else if (styleType === 'sphere') {
        viewer.value.setStyle({}, { sphere: { scale: 0.3 } });
      } else if (styleType === 'cross') {
        viewer.value.setStyle({}, { cross: { linewidth: 2 } });
      } 

      // Re-render the molecule
      viewer.value.render();
    };

    const downloadPDB = () => {
      const sanitizedFileName = molecule_name.value.replace(/\s+/g, '_') + '__Data.pdb'; // Adjust the filename as needed
      const downloadUrl = `http://127.0.0.1:5000/downloads/${sanitizedFileName}`;
      window.open(downloadUrl, '_blank'); // This will open the download in a new tab
    };

    const downloadChemReport = () => {
      const sanitizedFileName = molecule_name.value.replace(/\s+/g, '_') + '_report.pdf'; // download pdf report we generated
      const downloadUrl = `http://127.0.0.1:5000/downloads/${sanitizedFileName}`;
      window.open(downloadUrl, '_blank'); // open download in new tab
    };

    return {
      leftDrawerOpen,
      smiles,
      molecule_name,
      mol_block,
      molecularInfo,
      columns,
      splitModel,
      toggleLeftDrawer,
      generateMolecule,
      changeStyle,
      downloadPDB,
      downloadChemReport,
    };
  },
};
</script>

<style scoped>
/* Add any additional styles here */
</style>
