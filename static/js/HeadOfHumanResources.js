
import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            contract_templates: [],
            parameters: [],
            units: [],
            inspectors: [],
            parameter: {},
            isEditingParameter: false
        };
    },
    methods: {
        getContractTemplates() {
            axios.get('/contract-templates', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.contract_templates = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        onAddContractTemplate(){
            let template = prompt("Please enter template name", "");

            if (template != null) {
                let body = {"name": template}
                axios.post('/contract-templates', body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.getContractTemplates();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }
        },

        editContractTemplate(contract_template_id){
            let template = prompt("Please enter template name", "");

            if (template != null) {
                let body = {"name": template}
                axios.put('/contract-templates/' + contract_template_id, body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.getContractTemplates();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }
        },
        deleteContractTemplate(contract_template_id){
            if (!confirm('Do you want to delete template?')){
                return;
            }
            axios.delete('/contract-templates/' + contract_template_id, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getContractTemplates();
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },

        getParameters() {
            axios.get('/parameters', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.parameters = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        addParameter(){
            this.isEditingParameter = true;
            this.parameter = {};
        },

        editParameter(parameter){
            this.isEditingParameter = true;
            this.parameter = {"id":parameter.id, "name": parameter.name, "unit_id": parameter.unit_id, "inspector_id":parameter.inspector_id};
        },
        deleteParameter(parameter_id){
            if (!confirm('Do you want to delete parameter?')){
                return;
            }
            axios.delete('/parameters/' + parameter_id, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getParameters();
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },

        saveParameter() {
            let body = this.parameter;
            if(this.parameter.id == null){
                axios.post('/parameters', body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingParameter = false;
                    this.parameter = {};
                    this.getParameters();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }else{
                axios.put('/parameters/' + this.parameter.id, body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingParameter = false;
                    this.parameter = {};
                    this.getParameters();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }


        },
        cancelParameter() {
            this.isEditingParameter = false;
            this.parameter = {};
            this.getParameters();
//            this.$router.back();
        }
    },
    mounted() {
        this.getContractTemplates();
        this.getParameters();

        axios.get('/units', {
            headers: {
                'Token': Token.token,
            }
        })
        .then((res) => {
            this.units = res.data;
        })
        .catch((error) => {
          console.log(error.message);
        })

        axios.get('/inspectors', {
            headers: {
                'Token': Token.token,
            }
        })
        .then((res) => {
            this.inspectors = res.data;
        })
        .catch((error) => {
          console.log(error.message);
        })
    },
    template: `
        <button id="add-contract-template" v-on:click="onAddContractTemplate">Add contract template</button>
        <table id="contract-templates-list">
            <tr>
                <th>Name</th>
                <th></th>
                <th></th>
            </tr>
            <tr class="contract-templates-item" v-for="(item, index) in contract_templates" v-bind:id="item.id" v-bind:key="item.id">
                <td>{{ item.name }}</td>
                <td v-on:click="editContractTemplate(item.id)">Edit</td>
                <td v-on:click="deleteContractTemplate(item.id)">Delete</td>
            </tr>
        </table>

        <button id="add-parameter" v-on:click="addParameter">Add parameter</button>
        <table id="parameter-list">
            <tr>
                <th>Name</th>
                <th>Units</th>
                <th>Inspector</th>
                <th></th>
                <th></th>
            </tr>
            <tr class="parameter-item" v-for="(item, index) in parameters" v-bind:id="item.id" v-bind:key="item.id">
                <td>{{ item.name }}</td>
                <td>{{ item.unit }}</td>
                <td>{{ item.inspector }}</td>
                <td v-on:click="editParameter(item)">Edit</td>
                <td v-on:click="deleteParameter(item.id)">Delete</td>
            </tr>
        </table>

        <div id='edit-parameter' v-show="isEditingParameter">
            <label for="parameter-name">Full name:</label>
            <input id="parameter-name" required v-model="parameter.name">

            <label for="parameter-units">Unit:</label>
            <select name="parameter-units" id="parameter-units" v-model="parameter.unit_id">
                  <option value=""></option>
                  <option v-bind:value="item.id" v-for="(item, index) in units" v-bind:key="item.id">{{ item.name }}</option>
            </select>

            <label for="parameter-inspectors">Inspector:</label>
            <input id="parameter-inspectors" type="search" list="parameter-inspectors-list" v-model="parameter.inspector_id">
            <datalist id="parameter-inspectors-list">
              <option v-bind:value="item.id" v-for="(item, index) in inspectors" v-bind:key="item.id">{{ item.full_name }} ({{ item.id }})</option>
            </datalist>

            <button v-on:click="saveParameter">Save</button>
            <button v-on:click="cancelParameter">Cancel</button>

        </div>
    `,
};