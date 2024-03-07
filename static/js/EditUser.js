
import Token from './Token.js'

export default {
    props: ['id'],
    components: {

    },
    data() {
        return {
            user: {},
            passwordVal:"",
            job_titles: [],
            cathedras: []
        };
    },
    methods: {
        save() {
            let body = {"user": this.user, "password": this.passwordVal}
            axios.post('/users/' + this.id, body, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.$router.back();
            })
            .catch((error) => {
              console.log(error.message);
            })
        },
        cancel() {
            this.$router.back();
        },

        is_selected_job_title(item_id){
            return item_id === this.user.job_title_id ? "selected" : null;
        }

    },
    mounted() {
        axios.get('/job_titles', {
            headers: {
                'Token': Token.token,
            }
        })
        .then((res) => {
            this.job_titles = res.data;
        })
        .catch((error) => {
          console.log(error.message);
        })

        axios.get('/cathedras', {
            headers: {
                'Token': Token.token,
            }
        })
        .then((res) => {
            this.cathedras = res.data;
        })
        .catch((error) => {
          console.log(error.message);
        })

        if(this.id !== "new"){
            axios.get('/users/' + this.id, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.user = res.data;
            })
            .catch((error) => {
              console.log(error.message);
            })
        }
    },
    template: `
        <div>
            <label for="id">id:</label>
            <input id="id" required v-model="user.id">

            <label for="full-name">Full name:</label>
            <input id="full-name" required v-model="user.full_name">

            <label for="job-title">Job title:</label>
            <select name="job-title" id="job-title">
                  <option value=""></option>
                  <option v-bind:value="item.id" v-bind:[is_selected_job_title(item.id)] v-for="(item, index) in job_titles" v-bind:key="item.id">{{ item.name }}</option>
            </select>

            <label for="cathedra">Cathedra:</label>
            <select name="cathedra" id="cathedra">
                  <option value=""></option>
                  <option value="{{ item.id }}" v-for="(item, index) in cathedras" v-bind:key="item.id">{{ item.name }}</option>
            </select>

            <label for="role">Role:</label>
            <input id="role" required v-model="user.role">

            <label for="login">Login:</label>
            <input id="login" required v-model="user.login">

            <label for="password">New password:</label>
            <input id="password" v-model="passwordVal">

            <label for="email">Email:</label>
            <input id="email" required v-model="user.email">

            <button v-on:click="save">Save</button>
            <button v-on:click="cancel">Cancel</button>
        </div>
    `,
};