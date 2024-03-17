
import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            report_html_body: "",
            faculties: [],
            selectedFaculty: null,

            cathedras: [],
            teachers:[],
            extend: false,

            filter: {"from":"","till":"","faculty":null,"cathedra_id":null,"user_id":"","extended":false},
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
        },
        selectSigningReport(){
            this.selected_id = 'signing_progress';

        },
        getFaculties(){
            axios.get('/faculties', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.faculties = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        getCathedras(){
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
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
        getTeachers(){
            axios.get('/users', {
                params:{
                        faculty_id: this.filter.faculty_id,
                        cathedra_id : this.filter.cathedra_id,
                },
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.teachers = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },
    },
    mounted() {
        this.getFaculties();

    },
    template: `
        <div class="centered-div">
            <table>
                <tr>
                    <td>
                        <ul>
                            <li v-on:click="selectExecutionReport">execution progress</li>
                            <li v-on:click="selectSigningReport">signing progress</li>
                        </ul>
                    </td>
                    <td>
                       <div>
                            <label for="period-from">From:</label>
                            <input id="period-from" type="date" v-model="filter.from">
                            <label for="period-till">Till:</label>
                            <input id="period-till" type="date" v-model="filter.till">

                            <label for="faculty">Faculty:</label>

                            <p-dropdown v-model="filter.faculty" v-bind:options="faculties" filter optionLabel="name" placeholder="Select a Faculty" class="w-full md:w-14rem" v-on:change="getCathedras">
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

                            <label for="cathedras">Cathedra:</label>
                            <input id="cathedras" type="search" list="cathedras-list" @change="getTeachers" v-model="filter.cathedra_id">
                            <datalist id="cathedras-list">
                              <option v-bind:value="item.id" v-for="(item, index) in cathedras" v-bind:key="item.id">{{ item.name }} ({{ item.id }})</option>
                            </datalist>

                            <label for="user">User:</label>
                            <input id="user" type="search" list="users-list" v-model="filter.user_id">
                            <datalist id="users-list">

                              <option v-bind:value="item.id" v-for="(item, index) in teachers" v-bind:key="item.id">{{ item.name }} ({{ item.id }})</option>
                            </datalist>

                            <label for="extended-view">Extended view:</label>
                            <input id="extended-view" type="checkbox" v-model="filter.extended">

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
//                            <input id="faculty" type="search" list="faculty-list" @change="getCathedras" v-model="filter.faculty.id">
//                            <datalist id="faculty-list">
//                              <option v-bind:value="item.id" v-for="(item, index) in faculties" v-bind:key="item.id">{{ item.name }} ({{ item.id }})</option>
//                            </datalist>
