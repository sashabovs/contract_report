
import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            contract_templates: [],
            isEditingTemplate: false,
            contract_template: {},

            parameters: [],
            units: [],
            inspectors: [],
            parameter: {"inspector":{}},
            isEditingParameter: false,

            parameters_in_template: [],
            isEditingParameterInTemplate: false,
            inspection_periods:[],
            parameter_in_template: {"parameter":{}},
            selected_template: -1,

            contracts: [],
            contract: {"user":{}},
            teachers_without_contract: [],
            isEditingContract: false,

            isEditingReportParameters: false,
            selected_report : -1,
            reported_parameters: [],
            reports: [],

            period:{},
            periods:[],
            isEditingPeriod: false,
        };
    },
    methods: {
        selectContractTemplate(contract_template_id) {
            this.selected_template = contract_template_id;
            this.parameter_in_template={"parameter":{}};
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
        saveTemplate(){
            if(!this.contract_template.name){
                return;
            }
            if(!this.contract_template.id){
                let body = {"name": this.contract_template.name}
                axios.post('/contract-templates', body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.getContractTemplates();
                    this.isEditingTemplate=false;
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }else{
                let body = {"name": this.contract_template.name}
                axios.put('/contract-templates/' + this.contract_template.id, body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.getContractTemplates();
                    this.isEditingTemplate=false;
                })
                .catch((error) => {
                  console.log(error.response.data);
                })

            }
        },
        cancelTemplate() {
            this.isEditingTemplate = false;
            this.contract_template = {};
        },
        addTemplate(){
            this.isEditingTemplate = true;
            this.contract_template={name:"",id:""};
        },
        editTemplate(contract_template){
            this.isEditingTemplate = true;
            this.contract_template=contract_template;
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
        getPeriods() {
            axios.get('/periods', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.periods = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        addPeriod(){
            this.isEditingPeriod = true;
            this.period = {};
        },

        editPeriod(period){
            this.isEditingPeriod = true;
            this.period = {"id":period.id, "period": period.period, "time_of_opening": period.time_of_opening, "time_of_closing":period.time_of_closing};
        },
        deletePeriod(period_id){
            if (!confirm('Do you want to delete period?')){
                return;
            }
            axios.delete('/periods/' + period_id, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getPeriods();
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },

        savePeriod() {
            let body = this.period;
            if(this.period.id == null){
                axios.post('/periods', body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingPeriod = false;
                    this.period = {};
                    this.getPeriods();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }else{
                axios.put('/periods/' + this.period.id, body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingPeriod = false;
                    this.period = {};
                    this.getPeriods();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }


        },
        cancelPeriod() {
            this.isEditingPeriod = false;
            this.period = {};
            this.getPeriods();
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
            this.parameter = {"inspector":{}};
        },

        editParameter(parameter){
            this.isEditingParameter = true;
            this.parameter = {"id":parameter.id, "name": parameter.name, "unit_id": parameter.unit_id, "inspector":parameter.inspector};
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
                    this.parameter = {"inspector":{}};
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
                    this.parameter = {"inspector":{}};
                    this.getParameters();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }


        },
        cancelParameter() {
            this.isEditingParameter = false;
            this.parameter = {"inspector":{}};
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
            this.parameter_in_template = {"parameter":{}};
            this.parameter_in_template.template_id = this.selected_template;
        },


        editParameterToTemplate(parameter_in_template){
            this.isEditingParameterInTemplate = true;
            this.parameter_in_template = {"id":parameter_in_template.id, "template_id": this.selected_template, "parameter": parameter_in_template.parameter,
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
                    this.parameter_in_template = {"parameter":{}};
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
                    this.parameter_in_template = {"parameter":{}};
                    this.getParametersInTemplate(this.selected_template);
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }


        },
        cancelParameterToTemplate() {
            this.isEditingParameterInTemplate = false;
            this.parameter_in_template = {"parameter":{}};
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
            this.contract = {"user":{}};
        },


        editContract(contract){
            this.isEditingContract = true;
            this.contract = {"id":contract.id, "user": contract.user,
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
                    this.contract = {"user":{}};
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
                    this.contract = {"user":{}};
                    this.getContracts();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }


        },
        cancelContract() {
            this.isEditingContract = false;
            this.contract = {"user":{}};
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
        },
        cancelReportedParameter(){
            this.isEditingReportParameters = false;
            this.selected_report=-1;
        },
        downloadFile(reported_parameter){
            var base64ToArrayBuffer = function (base64) {
                var binaryString =  window.atob(base64);
                var binaryLen = binaryString.length;
                var bytes = new Uint8Array(binaryLen);
                for (var i = 0; i < binaryLen; i++)        {
                    var ascii = binaryString.charCodeAt(i);
                    bytes[i] = ascii;
                }
                return bytes;
            }

            var saveByteArray = (function () {
                var a = document.createElement("a");
                document.body.appendChild(a);
                a.style = "display: none";
                return function (data, name) {
                    var blob = new Blob(data, {type: "octet/stream"}),
                        url = window.URL.createObjectURL(blob);
                    a.href = url;
                    a.download = name;
                    a.click();
                    window.URL.revokeObjectURL(url);
                };
            }());
            axios.get('/reported-parameter-confirmations/' + reported_parameter.confirmation_file.id + '/download-file', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                let decoded_file = base64ToArrayBuffer(res.data.binary);
                saveByteArray([decoded_file], res.data.file_name);
            })
            .catch((error) => {
              console.log(error.response.data);
            })

        },
        signReport(report_id) {
            axios.post('/reports/' + report_id +'/sign', {}, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getReports();
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        selectReport(report_id){
            this.selected_report = report_id;
            this.getReportedParameters(report_id);
            this.isEditingReportParameters=true;
        },

        getReports() {
            axios.get('/reports', {
                params:{
                    is_active: true
                },
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.reports = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        getReportedParameters(report_id) {
            axios.get('/reported-parameters', {
                params:{
                    report_id: report_id
                },
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.reported_parameters = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        goToDataReports(){
            this.$router.replace('data-reports');
        }
    },
    mounted() {
        this.getContractTemplates();
        this.getParameters();
        this.getContracts();
        this.getTeachersWithoutContract();
        this.getReports();
        this.getPeriods();

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
        <div class="centered-div">
            <div class="section-header"><a v-on:click="goToDataReports">Data Reports</a></div>

            <div class="section-header">Template parameters</div>
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
                    <td>{{ item.inspector.full_name }}</td>
                    <td class="button-label" v-on:click="editParameter(item)">Edit</td>
                    <td class="button-label" v-on:click="deleteParameter(item.id)">Delete</td>
                </tr>
            </table>


            <div class="modal-background" v-show="isEditingParameter">
                <div class="fully-centered-div">
                    <div id='edit-parameter'>
                        <label for="parameter-name">Full name:</label>
                        <input id="parameter-name" required v-model="parameter.name">

                        <label for="parameter-units">Unit:</label>
                        <select name="parameter-units" id="parameter-units" v-model="parameter.unit_id">
                              <option value=""></option>
                              <option v-bind:value="item.id" v-for="(item, index) in units" v-bind:key="item.id">{{ item.name }}</option>
                        </select>

                        <br>
                        <label for="parameter-inspectors">Inspector:</label>

                        <p-dropdown v-model="parameter.inspector" v-bind:options="inspectors" filter optionLabel="full_name" placeholder="Select an Inspector" class="w-full md:w-14rem">
                            <template #value="slotProps">
                                <div v-if="slotProps.value" class="flex align-items-center">
                                    <div>{{ slotProps.value.full_name }}</div>
                                </div>
                                <span v-else>
                                    {{ slotProps.placeholder }}
                                </span>
                            </template>
                            <template #option="slotProps">
                                <div class="flex align-items-center">
                                    <div>{{ slotProps.option.full_name }}</div>
                                </div>
                            </template>
                        </p-dropdown>

                        <button v-on:click="saveParameter">Save</button>
                        <button v-on:click="cancelParameter">Cancel</button>

                    </div>
                </div>
            </div>


            <div class="section-header">Opened periods</div>
            <button id="add-period" v-on:click="addPeriod">Add period</button>
            <table>
                <tr>
                    <th>Period</th>
                    <th>Opens</th>
                    <th>Closes</th>
                    <th></th>
                    <th></th>
                </tr>
                <tr class="report-item" v-for="(item, index) in periods" v-bind:id="item.id" v-bind:key="item.id">
                    <td >{{ item.period }}</td>
                    <td>{{ item.time_of_opening }}</td>
                    <td>{{ item.time_of_closing }}</td>
                    <td class="button-label" v-on:click="editPeriod(item)">Edit</td>
                    <td class="button-label" v-on:click="deletePeriod(item.id)">Delete</td>
                </tr>
            </table>


            <div class="modal-background" v-show="isEditingPeriod">
                <div class="fully-centered-div" id='reported-parameters-div'>
                    <label for="period-date">Period:</label>
                    <input name="period-date" id="period-date" v-model="period.period" type="date"/>

                    <label for="opening-period-date">Opening:</label>
                    <input name="opening-period-date" id="opening-period-date" v-model="period.time_of_opening" type="date"/>

                    <label for="closing-period-date">Closing:</label>
                    <input name="closing-period-date" id="closing-period-date" v-model="period.time_of_closing" type="date"/>

                    <button v-on:click="savePeriod">Save</button>
                    <button v-on:click="cancelPeriod">Cancel</button>
                </div>
            </div>



            <div class="section-header">Contract templates</div>
            <button id="add-contract-template" v-on:click="addTemplate">Add contract template</button>
            <table id="contract-templates-list">
                <tr>
                    <th>Name</th>
                    <th></th>
                    <th></th>
                </tr>
                <tr class="contract-templates-item" v-bind:class="item.id == selected_template ? 'selected-row':''" v-for="(item, index) in contract_templates" v-bind:id="item.id" v-bind:key="item.id">
                    <td v-on:click="selectContractTemplate(item.id)">{{ item.name }}</td>
                    <td class="button-label" v-on:click="editTemplate(item)">Edit</td>
                    <td class="button-label" v-on:click="deleteContractTemplate(item.id)">Delete</td>
                </tr>
            </table>

            <div class="modal-background" v-show="isEditingTemplate">
                <div class="fully-centered-div" id='edit-contract-template'>
                    <label for="contract-template-name">Template name:</label>
                    <input name="contract-template-name" id="contract-template-name" v-model="contract_template.name" />
                    <br>
                    <button v-on:click="saveTemplate">Save</button>
                    <button v-on:click="cancelTemplate">Cancel</button>
                </div>
            </div>



            <div class="section-header">Parameter templates</div>
            <button id="add-parameter-to-template" v-on:click="addParameterToTemplate">Add parameter to template</button>
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
                    <td>{{ item.parameter.name }}</td>
                    <td>{{ item.needs_inspection }}</td>
                    <td>{{ item.inspection_period_name }}</td>
                    <td>{{ item.requirement }}</td>
                    <td>{{ item.points_promised }}</td>
                    <td class="button-label" v-on:click="editParameterToTemplate(item)">Edit</td>
                    <td class="button-label" v-on:click="deleteParameterToTemplate(item.id)">Delete</td>
                </tr>
            </table>


            <div class="modal-background" v-show="isEditingParameterInTemplate">
                <div class="fully-centered-div">
                    <div id='edit-parameter-in-template'>
                        <label for="parameter-in-template-parameters">Parameter:</label>


                        <p-dropdown v-model="parameter_in_template.parameter" v-bind:options="parameters" filter optionLabel="name" placeholder="Select a Parameter" class="w-full md:w-14rem">
                            <template #value="slotProps">
                                <div v-if="slotProps.value" class="flex align-items-center">
                                    <div>{{ slotProps.value.name }}</div>
                                </div>
                                <span v-else>
                                    {{ slotProps.placeholder }}
                                </span>
                            </template>
                            <template #option="slotProps">
                                <div class="flex align-items-center">
                                    <div>{{ slotProps.option.name }}</div>
                                </div>
                            </template>
                        </p-dropdown>




                        <label for="parameter-needs-inspection">Needs inspection:</label>
                        <input name="parameter-needs-inspection" id="parameter-needs-inspection" v-model="parameter_in_template.needs_inspection" type="checkbox"/>

                        <br>
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
                </div>
            </div>

            <div class="section-header">Contracts</div>
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
                    <td>{{ item.user.full_name }}</td>
                    <td>{{ item.signing_date }}</td>
                    <td>{{ item.valid_from }}-{{ item.valid_till }}</td>
                    <td>{{ item.template_name }}</td>
                    <td>{{ item.required_points }}</td>
                    <td class="button-label" v-on:click="editContract(item)">Edit</td>
                    <td class="button-label" v-on:click="deleteContract(item.id)">Delete</td>
                </tr>
            </table>

            <div class="modal-background" v-show="isEditingContract">
                <div class="fully-centered-div">
                    <div id='edit-contract'>
                        <label for="contract-user">Person:</label>

                        <p-dropdown v-model="contract.user" v-bind:options="teachers_without_contract" filter optionLabel="full_name" placeholder="Select a Teacher" class="w-full md:w-14rem">
                            <template #value="slotProps">
                                <div v-if="slotProps.value" class="flex align-items-center">
                                    <div>{{ slotProps.value.full_name }}</div>
                                </div>
                                <span v-else>
                                    {{ slotProps.placeholder }}
                                </span>
                            </template>
                            <template #option="slotProps">
                                <div class="flex align-items-center">
                                    <div>{{ slotProps.option.full_name }}</div>
                                </div>
                            </template>
                        </p-dropdown>



                        <label for="contract-signing-date">Signing date:</label>
                        <input name="contract-signing-date" id="contract-signing-date" v-model="contract.signing_date" type="date"/>
                        <br>
                        <label for="contract-valid-from">Valid from:</label>
                        <input name="contract-valid-from" id="contract-valid-from" v-model="contract.valid_from" type="date"/>
                        <br>
                        <label for="contract-valid-till">Valid till:</label>
                        <input name="contract-valid-till" id="contract-valid-till" v-model="contract.valid_till" type="date"/>
                        <br>
                        <label for="contract-template-select">Template:</label>
                        <select name="contract-template-select" id="contract-template-select" v-model="contract.template_id">
                              <option v-bind:value="item.id" v-for="(item, index) in contract_templates" v-bind:key="item.id">{{ item.name }}</option>
                        </select>

                        <br>
                        <label for="contract-points-required">Points required:</label>
                        <input id="contract-points-required" required v-model="contract.required_points">

                        <button v-on:click="saveContract">Save</button>
                        <button v-on:click="cancelContract">Cancel</button>

                    </div>
                </div>
            </div>

            <div class="section-header">Signatures</div>
            <table>
                <tr>
                    <th>Report period</th>
                    <th>Contract</th>
                    <th>Signed by teacher</th>
                    <th>Signed by head of cathedra</th>
                    <th>Signed by inspectors</th>
                    <th>Signed by head of human resources</th>
                    <th></th>
                </tr>
                <tr class="report-item" v-for="(item, index) in reports" v-bind:id="item.id" v-bind:key="item.id">
                    <td v-on:click="selectReport(item.id)">{{ item.period_of_report }}</td>
                    <td>{{ item.contract.name }}</td>
                    <td>{{ item.signed_by_teacher }}</td>
                    <td>{{ item.signed_by_head_of_cathedra }}</td>
                    <td>{{ item.signed_by_inspector }}</td>
                    <td>{{ item.signed_by_head_of_human_resources }}</td>
                    <td class="button-label" v-on:click="signReport(item.id)">Sign</td>
                </tr>
            </table>


            <div class="modal-background" v-show="isEditingReportParameters">
                <div class="fully-centered-div" id='reported-parameters-div'>
                    <table id="reported-parameters-list">
                        <tr>
                            <th>Parameter name</th>
                            <th>Done</th>
                            <th>Confirmation</th>
                            <th>Inspectors comment</th>
                            <th>Signed by inspector</th>
                        </tr>
                        <tr class="reported-parameter-item" v-for="(item, index) in reported_parameters" v-bind:id="item.id" v-bind:key="item.id">
                            <td>{{ item.parameter_name }}</td>
                            <td><input v-model="item.done"></td>
                            <td><input v-model="item.confirmation_text">
                                <input v-bind:id="'upload-file-' + index"
                                  type="file"
                                  @change="onFileChanged(item, $event)"
                                  capture
                                />
                                <label v-if="item.confirmation_file" v-on:click="downloadFile(item)">{{ item.confirmation_file.file_name }}</label>
                            </td>
                            <td>{{ item.inspector_comment }}</td>
                            <td>{{ item.signed_by_inspector }}</td>
                        </tr>
                    </table>
                    <button v-on:click="cancelReportedParameter">Cancel</button>
                </div>
            </div>

        </div>
    `,
};

