
import Token from './Token.js'

export default {
    props: ['id'],
    components: {

    },
    data() {
        return {
            user: {},
//            idVal:"",
//            fullNameVal:"",
//            jobTitleVal:"",
//            cathedraVal:"",
//            roleVal:"",
//            loginVal:"",
            passwordVal:"",
//            emailVal:""
        };
    },
    methods: {
        save() {

        },
        cancel() {
        }
    },
    mounted() {
        axios.get('/users/' + this.id, {
            headers: {
                'Token': Token.token,
            }
        })
        .then((res) => {
            this.user = res.data;
        })
        .catch((error) => {
          console.log(error.data.message);
        })
    },
    template: `
        <div>
            <label for="id">id:</label>
            <input id="id" required v-model="user.id">

            <label for="full-name">Full name:</label>
            <input id="full-name" required v-model="user.full_name">

            <button v-on:click="save">Save</button>
            <button v-on:click="cancel">Cancel</button>
        </div>
    `,
};