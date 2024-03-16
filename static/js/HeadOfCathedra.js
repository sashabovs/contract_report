import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            isEditingReport: false,
            isEditingReportParameters: false,
            reports: [],
            report: {"signed_by_teacher":false, "signed_by_head_of_cathedra":false, "signed_by_head_of_human_resources":false},

            reported_parameters: [],



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

        },


        editReport(report){
        },


        deleteReport(report_id){

        },

        saveReport() {
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

        },
        cancelReportedParameter() {
            this.isEditingReportParameters = false;
            this.selected_report=-1;
        },

        onFileChanged(item, event) {

        }
    },
    mounted() {
        var token_data = Token.getTokenData();
        this.user_id = token_data.user_id;
        this.getReports();
    },
    template: `
        <div class="centered-div">
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
                    <button v-on:click="saveReportedParameters">Save</button>
                    <button v-on:click="cancelReportedParameter">Cancel</button>
                </div>
            </div>
        </div>
    `,
};

//                    <form action='/upload_file' method='post' enctype='multipart/form-data' v-bind:name="'upload-file-' + index">
