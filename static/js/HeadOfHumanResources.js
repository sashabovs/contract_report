
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
            isEditingParameter: false,

            parameters_in_template: [],
            isEditingParameterInTemplate: false,
            inspection_periods:[],
            parameter_in_template: {},
            selected_template: -1,

            contracts: [],
            contract: {},
            teachers_without_contract: [],
            isEditingContract: false,
        };
    },
    methods: {
        selectContractTemplate(contract_template_id) {
            this.selected_template = contract_template_id;
            this.parameter_in_template={};
            this.isEditingParameterInTemplate = false;
            this.getParametersInTemplate(contract_template_id);
        },
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
        },
        getParametersInTemplate(contract_template_id) {
            axios.get('/parameters-in-template/' + contract_template_id, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.parameters_in_template = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        addParameterToTemplate(){
            if(this.selected_template == -1){
                alert("Template is not selected! Please click on template name");
                return;
            }
            this.isEditingParameterInTemplate = true;
            this.parameter_in_template = {};
            this.parameter_in_template.template_id = this.selected_template;
        },


        editParameterToTemplate(parameter_in_template){
            this.isEditingParameterInTemplate = true;
            this.parameter_in_template = {"id":parameter_in_template.id, "template_id": this.selected_template, "parameter_id": parameter_in_template.parameter_id,
            "needs_inspection": parameter_in_template.needs_inspection, "inspection_period_id":parameter_in_template.inspection_period_id,
            "requirement":parameter_in_template.requirement, "points_promised":parameter_in_template.points_promised};
        },
        deleteParameterToTemplate(parameter_in_template_id){
            if (!confirm('Do you want to delete parameter from template?')){
                return;
            }
            axios.delete('/parameters-in-template/' + parameter_in_template_id, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getParametersInTemplate(this.selected_template);
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },

        saveParameterToTemplate() {
            let body = this.parameter_in_template;
            if(this.parameter_in_template.id == null){
                axios.post('/parameters-in-template', body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingParameterInTemplate = false;
                    this.parameter_in_template = {};
                    this.getParametersInTemplate(this.selected_template);
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }else{
                axios.put('/parameters-in-template/' + this.parameter_in_template.id, body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingParameterInTemplate = false;
                    this.parameter_in_template = {};
                    this.getParametersInTemplate(this.selected_template);
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }


        },
        cancelParameterToTemplate() {
            this.isEditingParameterInTemplate = false;
            this.parameter_in_template = {};
            this.getParametersInTemplate(this.selected_template);
        },


        getContracts() {
            axios.get('/contracts', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.contracts = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        addContract(){
            this.isEditingContract = true;
            this.contract = {};
        },


        editContract(contract){
            this.isEditingContract = true;
            this.contract = {"id":contract.id, "user_id": contract.user_id,
            "signing_date": contract.signing_date, "valid_from":contract.valid_from,
            "valid_till":contract.valid_till, "template_id":contract.template_id, "required_points":contract.required_points};
        },


        deleteContract(contract_id){
            if (!confirm('Do you want to delete parameter from template?')){
                return;
            }
            axios.delete('/contracts/' + contract_id, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getContracts();
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },

        saveContract() {
            let body = this.contract;
            if(this.contract.id == null){
                axios.post('/contracts', body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingContract = false;
                    this.contract = {};
                    this.getContracts();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }else{
                axios.put('/contracts/' + this.contract.id, body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingContract = false;
                    this.contract = {};
                    this.getContracts();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }


        },
        cancelContract() {
            this.isEditingContract = false;
            this.contract = {};
            this.getContracts();
        },
        getTeachersWithoutContract(){
            axios.get('/teachers-without-contract', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.teachers_without_contract = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        }
    },
    mounted() {
        this.getContractTemplates();
        this.getParameters();
        this.getContracts();
        this.getTeachersWithoutContract();

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

        axios.get('/inspection-periods', {
            headers: {
                'Token': Token.token,
            }
        })
        .then((res) => {
            this.inspection_periods = res.data;
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
                <td v-on:click="selectContractTemplate(item.id)">{{ item.name }}</td>
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
        ///////////////////////////////////////////

        <button id="add-parameter-to-template" v-on:click="addParameterToTemplate">Add parameter</button>
        <table id="parameters-in-template-list">
            <tr>
                <th>Name</th>
                <th>Needs inspection</th>
                <th>Inspection period</th>
                <th>Requirement</th>
                <th>Points promised</th>
                <th></th>
                <th></th>
            </tr>
            <tr class="parameters-in-template-item" v-for="(item, index) in parameters_in_template" v-bind:id="item.id" v-bind:key="item.id">
                <td>{{ item.parameter_name }}</td>
                <td>{{ item.needs_inspection }}</td>
                <td>{{ item.inspection_period_name }}</td>
                <td>{{ item.requirement }}</td>
                <td>{{ item.points_promised }}</td>
                <td v-on:click="editParameterToTemplate(item)">Edit</td>
                <td v-on:click="deleteParameterToTemplate(item.id)">Delete</td>
            </tr>
        </table>

        <div id='edit-parameter-in-template' v-show="isEditingParameterInTemplate">
            <label for="parameter-in-template-parameters">Parameter:</label>
            <input id="parameter-in-template-parameters" type="search" list="parameter-in-template-list" v-model="parameter_in_template.parameter_id">
            <datalist id="parameter-in-template-list">
              <option v-bind:value="item.id" v-for="(item, index) in parameters" v-bind:key="item.id">{{ item.name }} ({{ item.id }})</option>
            </datalist>


            <label for="parameter-needs-inspection">Needs inspection:</label>
            <input name="parameter-needs-inspection" id="parameter-needs-inspection" v-model="parameter_in_template.needs_inspection" type="checkbox"/>

            <label for="parameter-in-template-inspection-periods">Inspection period:</label>
            <select name="parameter-in-template-inspection-periods" id="parameter-in-template-inspection-periods" v-model="parameter_in_template.inspection_period_id">
                  <option value=""></option>
                  <option v-bind:value="item.id" v-for="(item, index) in inspection_periods" v-bind:key="item.id">{{ item.name }}</option>
            </select>

            <label for="parameter-in-template-required">Requirements:</label>
            <input id="parameter-in-template-required" required v-model="parameter_in_template.requirement">

            <label for="parameter-in-template-points-promised">Points promised:</label>
            <input id="parameter-in-template-points-promised" required v-model="parameter_in_template.points_promised">

            <button v-on:click="saveParameterToTemplate">Save</button>
            <button v-on:click="cancelParameterToTemplate">Cancel</button>

        </div>


        <button id="add-contract" v-on:click="addContract">Add contract</button>
        <table id="contracts-list">
            <tr>
                <th>Person</th>
                <th>Signing date</th>
                <th>Valid period</th>
                <th>Template</th>
                <th>Required points</th>
                <th></th>
                <th></th>
            </tr>
            <tr class="contract-item" v-for="(item, index) in contracts" v-bind:id="item.id" v-bind:key="item.id">
                <td>{{ item.user_name }}</td>
                <td>{{ item.signing_date }}</td>
                <td>{{ item.valid_from }}-{{ item.valid_till }}</td>
                <td>{{ item.template_name }}</td>
                <td>{{ item.required_points }}</td>
                <td v-on:click="editContract(item)">Edit</td>
                <td v-on:click="deleteContract(item.id)">Delete</td>
            </tr>
        </table>

        <div id='edit-contract' v-show="isEditingContract">
            <label for="contract-user">Person:</label>
            <input id="contract-user" type="search" list="user-list" v-model="contract.user_id">
            <datalist id="user-list">
              <option v-bind:value="item.id" v-for="(item, index) in teachers_without_contract" v-bind:key="item.id">{{ item.name }} ({{ item.id }})</option>
            </datalist>


            <label for="contract-signing-date">Signing date:</label>
            <input name="contract-signing-date" id="contract-signing-date" v-model="contract.signing_date" type="date"/>

            <label for="contract-valid-from">Valid from:</label>
            <input name="contract-valid-from" id="contract-valid-from" v-model="contract.valid_from" type="date"/>

            <label for="contract-valid-till">Valid till:</label>
            <input name="contract-valid-till" id="contract-valid-till" v-model="contract.valid_till" type="date"/>

            <label for="contract-template-select">Template:</label>
            <select name="contract-template-select" id="contract-template-select" v-model="contract.template_id">
                  <option v-bind:value="item.id" v-for="(item, index) in contract_templates" v-bind:key="item.id">{{ item.name }}</option>
            </select>


            <label for="contract-points-required">Points required:</label>
            <input id="contract-points-required" required v-model="contract.required_points">

            <button v-on:click="saveContract">Save</button>
            <button v-on:click="cancelContract">Cancel</button>

        </div>
    `,
};

