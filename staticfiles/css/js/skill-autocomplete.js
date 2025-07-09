

document.addEventListener('DOMContentLoaded', function(){
    const skillInputs = document.querySelectorAll('.skill-autocomplete');

    skillInputs.forEach(input => {
        new Awesomplete(input, {
            minChars: 1,
            maxItems: 10,
            autoFirst: true,
            list: [],
            filter: function(text, input){
                return Awesomplete.FILTER_CONTAINS(text, input.match(/[^,]*$/)[0]);
            },
            item: function(text, input){
                return Awesomplete.ITEM(text, input.match(/[^,]*$/)[0]);
            },
            replace: function(text){
                const before = this.input.value.match(/^.+,\s*|/)[0];
                this.input.value = before + text + ", ";
            }
        });

        //fetch suggestions from server
        input.addEventListener('input', function(){
            const url = input.dataset.url + '?term=' + encodeURIComponent(input.value);
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    const awesomplete = input.awesomplete;
                    awesomplete.list = data;
                });
        });
    });
});