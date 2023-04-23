function lenght(array) {
    var len = 0;

    if (typeof array == "object") {
        if (Array.isArray(array)) {
            array.forEach(function (item) {
                len++;
            })
        } else {
            len = lenght(Object.keys(array));
        }
    }
    return len;
}

// Empty array's content
function empty(array){
    return array.splice(0,lenght(array))
}

const app = new Vue({
    el: "#app",
    data: {
        results: []
    },
    created: () => {


    },
    beforeMount: () => {



    },
    mounted: () => {
        Vue.nextTick(function () {
            app.get_results();
        })
    },
    methods: {
        get_results: () => {
            $.ajax({
                url: "http://localhost:8080/results",
                type: "GET",
                dataType: "json",
                success: (data) => {
                    app.results = data["results"];
                    console.log(data);
                }
            })
        },
        scan: () => {
            $.ajax({
                url: "http://localhost:8080/scan",
                type: "GET",
                dataType: "json",
                success: (data) => {
                    console.log(data);
                }
            })
        }
    },
    updated: () => {

    },
});