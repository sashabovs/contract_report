import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {

            reported_parameters: [],
            user_id : -1,
            isEditingInspectorsComment: false,
            inspector_comment: "",
            reported_parameter_id: -1,
        };
    },
    methods: {
        selectReport(report_id){

        },
        getContracts() {

        },
        getReports() {

        },
        getReportedParameters() {
            axios.get('/reported-parameters', {
                params:{
                    inspector_id: this.user_id
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

        },
        acceptReportedParameter(report_id) {
            axios.post('/reported-parameters/' + report_id +'/sign', {}, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getReportedParameters();
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        denyReportedParameter(report_id) {
            axios.delete('/reports/' + report_id +'/sign',  {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getReportedParameters();
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

        },

        onFileChanged(item, event) {

        },
        onAddCommentClick(reported_parameter_id, comment){
            this.isEditingInspectorsComment = true;
            this.reported_parameter_id = reported_parameter_id;
            this.inspector_comment = comment;
        },
        saveComment(){
            this.isEditingInspectorsComment = false;
            let body = {"inspector_comment":this.inspector_comment};
            axios.post('/reported-parameter/' + this.reported_parameter_id + '/save-comment',body, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getReportedParameters();
                this.inspector_comment = "";
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        cancelComment(){
            this.isEditingInspectorsComment = false;
            this.inspector_comment = "";
        }
    },
    mounted() {
        var token_data = Token.getTokenData();
        this.user_id = token_data.user_id;
        this.getReportedParameters();

    },
    template: `
        <div class="centered-div">

            <table id="reported-parameters-list">
                <tr>
                    <th>User</th>
                    <th>Parameter name</th>
                    <th>Done</th>
                    <th>Confirmation</th>
                    <th>Inspectors comment</th>
                    <th></th>
                    <th></th>
                </tr>
                <tr class="reported-parameter-item" v-for="(item, index) in reported_parameters" v-bind:id="item.id" v-bind:key="item.id">
                    <td>{{ item.full_name }}</td>
                    <td>{{ item.parameter_name }}</td>
                    <td>{{ item.done }}</td>
                    <td><input v-model="item.confirmation_text" readonly>
                        <input v-bind:id="'upload-file-' + index"
                          type="file"
                          @change="onFileChanged(item, $event)"
                          capture
                        />
                        <label v-if="item.confirmation_file" v-on:click="downloadFile(item)">{{ item.confirmation_file.file_name }}</label>
                    </td>
                    <td>{{ item.inspector_comment }}<button v-on:click="onAddCommentClick(item.id, item.inspector_comment)">Change comment</button></td>
                    <td class="button-label" v-on:click="acceptReportedParameter(item.id)">Accept</td>
                    <td class="button-label" v-on:click="denyReportedParameter(item.report_id)">Deny</td>
                </tr>
            </table>



            <div class="modal-background" v-show="isEditingInspectorsComment">
                <div class="fully-centered-div" id='reported-parameters-div'>
                    <input v-model="inspector_comment">
                    <br>
                    <button v-on:click="saveComment">Save comment</button>
                    <button v-on:click="cancelComment">Cancel</button>
                </div>
            </div>

        </div>
    `,
};

//                    <form action='/upload_file' method='post' enctype='multipart/form-data' v-bind:name="'upload-file-' + index">
