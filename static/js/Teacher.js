import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            isEditingReport: false,
            reports: [],
            report: {"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false},

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
            this.report = {"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false};
        },


        editReport(report){
            this.isEditingReport = true;
            this.report = {"id":report.id, "period_of_report": report.period_of_report,
            "contract_id": report.contract_id, "signed_by_teacher":report.signed_by_teacher,
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
                    this.report = {"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false};
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
                    this.report = {"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false};
                    this.getReports();
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }


        },
        cancelReport() {
            this.isEditingReport = false;
            this.report = {"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false};
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

//                    await fetch('/upload_file', {
//                      method: "POST",
//                      body: formData
//                    });

                    axios.post('reported-parameters/' + this.reported_parameters[i].id + '/upload_file', formData, {
                        headers: {
                            'Token': Token.token,
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    .then((res) => {
//                        this.getReportedParameters(this.selected_report);
                    })
                    .catch((error) => {
                      console.log(error.response.data);
                    })

//                    document["upload-file-" + i].submit();
                }

            }
        },

        onFileChanged(item, event) {
            if (event.target.files) {
                item.is_file_changed = true
            }
        }
    },
    mounted() {
        var token_data = Token.getTokenData();
        this.user_id = token_data.user_id;
        this.getReports();
        this.getContracts();
    },
    template: `
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
                <td v-on:click="selectReport(item.id)">{{ item.period_of_report }}</td>
                <td>{{ item.contract_name }}</td>
                <td>{{ item.signed_by_teacher }}</td>
                <td>{{ item.signed_by_head_of_cathedra }}</td>
                <td>{{ item.signed_by_inspectors }}</td>
                <td>{{ item.signed_by_head_of_human_resources }}</td>
                <td v-on:click="editReport(item)">Edit</td>
                <td v-on:click="deleteReport(item.id)">Delete</td>
                <td v-on:click="signReport(item.id)">Sign</td>
            </tr>
        </table>

        <div id='edit-report' v-show="isEditingReport">
            <label for="report-period-date">Report period:</label>
            <input name="report-period-date" id="report-period-date" v-model="report.period_of_report" type="date"/>

            <label for="report-contract">Contract:</label>
            <input id="report-contract" type="search" list="contracts-list" v-model="report.contract_id">
            <datalist id="contracts-list">
              <option v-bind:value="item.id" v-for="(item, index) in contracts" v-bind:key="item.id">{{ item.name }} ({{ item.id }})</option>
            </datalist>


            <button v-on:click="saveReport">Save</button>
            <button v-on:click="cancelReport">Cancel</button>

        </div>


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
        <button v-on:click="saveReportedParameters">Save</button>

    `,
};

//                    <form action='/upload_file' method='post' enctype='multipart/form-data' v-bind:name="'upload-file-' + index">