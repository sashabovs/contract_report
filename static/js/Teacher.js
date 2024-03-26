import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            isEditingReport: false,
            isEditingReportParameters: false,
            reports: [],
            report: {"period_of_report":{},"contract":{},"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false},
            periods_of_report:[],

            reported_parameters: [],

            contracts: [],

            selected_report: -1,
            user_id : -1,
        };
    },
    methods: {
        selectReport(report_id){
            this.selected_report = report_id;
            this.getReportedParameters(report_id);
            this.isEditingReportParameters=true;
        },
        getPeriodsOfReport() {
            axios.get('/periods', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.periods_of_report = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        getContracts() {
            axios.get('/contracts', {
                params:{
                    user_id: this.user_id,
                    is_active: true
                },
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
        getReports() {
            axios.get('/reports', {
                params:{
                    user_id: this.user_id,
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
        onAddReportClick(){
            this.isEditingReport = true;
            this.report = {"period_of_report":{},"contract":{},"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false};
        },


        editReport(report){
            this.isEditingReport = true;
            this.report = {"id":report.id, "period_of_report": report.period_of_report,
            "contract": report.contract, "signed_by_teacher":report.signed_by_teacher,
            "signed_by_head_of_cathedra":report.signed_by_head_of_cathedra,
            "signed_by_head_of_human_resources":report.signed_by_head_of_human_resources};
        },


        deleteReport(report_id){
            if (!confirm('Do you want to delete parameter from template?')){
                return;
            }
            axios.delete('/reports/' + report_id, {
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

        saveReport() {
            let body = this.report;
            if(this.report.id == null){
                axios.post('/reports', body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingReport = false;
                    this.report = {"period_of_report":{},"contract":{},"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false};
                    this.getReports();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }else{
                axios.put('/reports/' + this.report.id, body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.isEditingReport = false;
                    this.report = {"period_of_report":{},"contract":{},"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false};
                    this.getReports();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }


        },
        cancelReport() {
            this.isEditingReport = false;
            this.report = {"period_of_report":{},"contract":{},"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false};
            this.getReports();
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
        saveReportedParameters(){
            if(this.selected_report == -1){
                return;
            }

            let body = this.reported_parameters;
            axios.put('/reported-parameters', body, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getReportedParameters(this.selected_report);
                this.isEditingReportParameters=false;
            })
            .catch((error) => {
              console.log(error.response.data);
            })

            for (let i = 0; i < this.reported_parameters.length; i++) {
                if (this.reported_parameters[i].is_file_changed === true) {
                    let formData = new FormData();
                    formData.append("file", document.getElementById("upload-file-" + i).files[0]);
                    if(this.reported_parameters[i].confirmation_file){
                        formData.append("reported_parameter_confirmation_id", this.reported_parameters[i].confirmation_file.id);
                    }

                    axios.post('reported-parameters/' + this.reported_parameters[i].id + '/upload_file', formData, {
                        headers: {
                            'Token': Token.token,
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    .then((res) => {

                    })
                    .catch((error) => {
                      console.log(error.response.data);
                    })
                }
            }
        },
        cancelReportedParameter() {
            this.isEditingReportParameters = false;
            this.selected_report=-1;
        },

        onFileChanged(item, event) {
            if (event.target.files) {
                item.is_file_changed = true
            }
        },
        goToDataReports(){
            this.$router.replace('data-reports');
        }
    },
    mounted() {
        var token_data = Token.getTokenData();
        this.user_id = token_data.user_id;
        this.getReports();
        this.getContracts();
        this.getPeriodsOfReport();
    },
    template: `
        <div class="centered-div">
            <div class="section-header"><a v-on:click="goToDataReports">Data Reports</a></div>

            <button id="add-report" v-on:click="onAddReportClick">Add report</button>
            <table id="reports-list">
                <tr>
                    <th>Report period</th>
                    <th>Contract</th>
                    <th>Signed by teacher</th>
                    <th>Signed by head of cathedra</th>
                    <th>Signed by inspectors</th>
                    <th>Signed by head of human resources</th>
                    <th></th>
                    <th></th>
                    <th></th>
                </tr>
                <tr class="report-item" v-for="(item, index) in reports" v-bind:id="item.id" v-bind:key="item.id">
                    <td class="button-label" v-on:click="selectReport(item.id)">{{ item.period_of_report }}</td>
                    <td>{{ item.contract.name }}</td>
                    <td>{{ item.signed_by_teacher }}</td>
                    <td>{{ item.signed_by_head_of_cathedra }}</td>
                    <td>{{ item.signed_by_inspector }}</td>
                    <td>{{ item.signed_by_head_of_human_resources }}</td>
                    <td class="button-label" v-on:click="editReport(item)">Edit</td>
                    <td class="button-label" v-on:click="deleteReport(item.id)">Delete</td>
                    <td class="button-label" v-on:click="signReport(item.id)">Sign</td>
                </tr>
            </table>

            <div class="modal-background" v-show="isEditingReport">
                <div class="fully-centered-div" id='edit-report'>
                    <label for="report-period-date">Report period:</label>

                    <p-dropdown v-model="report.period_of_report" v-bind:options="periods_of_report" filter optionLabel="period" placeholder="Select a Period" class="w-full md:w-14rem">
                        <template #value="slotProps">
                            <div v-if="slotProps.value" class="flex align-items-center">
                                <div>{{ slotProps.value.period }}</div>
                            </div>
                            <span v-else>
                                {{ slotProps.placeholder }}
                            </span>
                        </template>
                        <template #option="slotProps">
                            <div class="flex align-items-center">
                                <div>{{ slotProps.option.period }}</div>
                            </div>
                        </template>
                    </p-dropdown>

                    <br>
                    <label for="report-contract">Contract:</label>


                    <p-dropdown v-model="report.contract" v-bind:options="contracts" filter optionLabel="name" placeholder="Select a Contract" class="w-full md:w-14rem">
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



                    <button v-on:click="saveReport">Save</button>
                    <button v-on:click="cancelReport">Cancel</button>

                </div>
            </div>

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
                            <td v-bind:class="item.parameter_requirement_fulfilled ? 'parameter-requirement-fulfilled':''">{{ item.parameter_name }}</td>
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
                    <button v-on:click="saveReportedParameters">Save</button>
                    <button v-on:click="cancelReportedParameter">Cancel</button>
                </div>
            </div>
        </div>
    `,
};

//                    <form action='/upload_file' method='post' enctype='multipart/form-data' v-bind:name="'upload-file-' + index">
