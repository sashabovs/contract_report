
import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            report_html_body: "",
            faculties: [],


            cathedras: [],
            teachers:[],
            extend: false,

            filter: {"from":"","till":"","faculty":{},"cathedra":{},"user":{},"extended":false},
            selected_id: "",
        };
    },
    methods: {
        fillReport() {
            let body = this.filter;
            axios.put('/data-reports/' + this.selected_id, body,{
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.report_html_body = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        selectExecutionReport(){
            this.selected_id = 'execution_progress';

            var token_data = Token.getTokenData();
            if(['teacher', 'head_of_cathedra'].includes(token_data.role)){
                this.filter.faculty.id = token_data.faculty_id;
                this.filter.cathedra.id = token_data.cathedra_id;
                this.getTeachers();
            }
            if(['teacher'].includes(token_data.role)){
                this.filter.user.id = token_data.user_id;
            }
        },
        selectSigningReport(){
            this.selected_id = 'signing_progress';

        },
        selectSigningLogReport(){
            this.selected_id = 'signing_log';
        },
        selectDataChangeLogReport(){
            this.selected_id = 'data_change_log';
        },
        getFaculties(){
            axios.get('/faculties', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.faculties = res.data;
                this.faculties.splice(0, 0, {});
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        getCathedras(){
            this.filter.cathedra = {};
            this.filter.user = {};
            this.cathedras = [];
            this.teachers = [];

            if (!this.filter.faculty) {
                return
            }
            axios.get('/cathedras', {
                params:{
                        faculty_id: this.filter.faculty.id,
                },
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.cathedras = res.data;
                this.cathedras.splice(0, 0, {});
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        getTeachers(){
            this.filter.user = {};
            this.teachers = [];
            if (!this.filter.cathedra || !this.filter.faculty) {
                return
            }
            axios.get('/users', {
                params:{
                        faculty_id: this.filter.faculty.id,
                        cathedra_id : this.filter.cathedra.id,
                        role: 'teacher',
                },
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.teachers = res.data;
                this.teachers.splice(0, 0, {});
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        showReport(reportName){
            if(['signing_progress', 'signing_log', 'data_change_log'].includes(reportName)){
                var token_data = Token.getTokenData();

                return token_data.role === "head_of_human_resources";
            }
        },
        showFilterItem(item){
            var token_data = Token.getTokenData();
            var role = token_data.role;

            if(this.selected_id == 'signing_progress'){
                return ['period-from', 'period-till', 'faculty', 'cathedras', 'user'].includes(item);
            }else if(this.selected_id == 'execution_progress'){
                if(role == 'teacher'){
                    var bla = ['period-from', 'period-till', 'extended-view'].includes(item);
                    return ['period-from', 'period-till', 'extended-view'].includes(item);
                }else if(role == 'head_of_cathedra'){
                    return ['period-from', 'period-till', 'user', 'extended-view'].includes(item);
                }else if(role == 'head_of_human_resources'){
                    return ['period-from', 'period-till', 'faculty', 'cathedras', 'user', 'extended-view'].includes(item);
                }

            }else if(this.selected_id == 'signing_log' || this.selected_id == 'data_change_log'){
                return ['period-from', 'period-till'].includes(item);

            }

        }
    },
    mounted() {
        this.getFaculties();

    },
    template: `
        <div class="centered-div">
            <table id="data-reports-main-table">
                <tr>
                    <td>
                        <ul>
                            <li v-on:click="selectExecutionReport" v-bind:class="'execution_progress' == selected_id ? 'selected-row':''">execution progress</li>
                            <li v-on:click="selectSigningReport" v-bind:class="'signing_progress' == selected_id ? 'selected-row':''" v-if="showReport('signing_progress')">signing progress</li>
                            <li v-on:click="selectSigningLogReport" v-bind:class="'signing_log' == selected_id ? 'selected-row':''" v-if="showReport('signing_log')">signing log</li>
                            <li v-on:click="selectDataChangeLogReport" v-bind:class="'data_change_log' == selected_id ? 'selected-row':''" v-if="showReport('data_change_log')">data change log</li>
                        </ul>
                    </td>
                    <td>
                       <div>
                            <label for="period-from" v-if="showFilterItem('period-from')">From:</label>
                            <input id="period-from" type="date" v-model="filter.from" v-if="showFilterItem('period-from')">
                            <label for="period-till" v-if="showFilterItem('period-till')">Till:</label>
                            <input id="period-till" type="date" v-model="filter.till" v-if="showFilterItem('period-till')">

                            <label for="faculty" v-if="showFilterItem('faculty')">Faculty:</label>

                            <p-dropdown v-model="filter.faculty" v-bind:options="faculties" filter optionLabel="name" placeholder="Select a Faculty" class="w-full md:w-14rem" v-on:change="getCathedras" v-if="showFilterItem('faculty')">
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

                            <label for="cathedras" v-if="showFilterItem('cathedras')">Cathedra:</label>

                            <p-dropdown v-model="filter.cathedra" v-bind:options="cathedras" filter optionLabel="name" placeholder="Select a Cathedra" class="w-full md:w-14rem" v-on:change="getTeachers" v-if="showFilterItem('cathedras')">
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


                            <label for="user" v-if="showFilterItem('user')">User:</label>

                            <p-dropdown v-model="filter.user" v-bind:options="teachers" filter optionLabel="full_name" placeholder="Select a User" class="w-full md:w-14rem" v-if="showFilterItem('user')">
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


                            <label for="extended-view" v-if="showFilterItem('extended-view')">Extended view:</label>
                            <input id="extended-view" type="checkbox" v-model="filter.extended" v-if="showFilterItem('extended-view')">

                            <br>
                            <button v-on:click="fillReport">Fill</button>
                        </div>

                        <div id="report-body" v-html="report_html_body">

                        </div>
                    </td>
                </tr>
            </table>
        </div>
    `,
};

