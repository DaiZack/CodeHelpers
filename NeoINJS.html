    <script>
        $(function(){
                var fbid = {{ data }}
            console.log(fbid);
            var body = JSON.stringify({
                            statements: [{
                                statement: 'MATCH (f:FBterm {id:"'+fbid.toString()+'"}) RETURN f.id'
                                }]
                            });
            console.log(body);

                $.ajax({
                    url: "http://localhost:7474/db/data/transaction/commit",
                    type: "POST",
                    data: body,
                    contentType: "application/json",
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader ("Authorization", "Basic " + btoa("userName"+ ":" + "password"));
                    }}
                    )
                    .done(function(result){
                         console.log(result.data);
                    })
                    .fail(function(error){
                        console.log(error.statusText);
                    });

            })
    </script>
