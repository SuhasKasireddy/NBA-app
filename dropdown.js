function cleardropdown()
{
    const teamInput = document.getElementById("team-input");
    const playerInput = document.getElementById("player-input");
    teamInput.value = ""
    playerInput.value = ""
    document.getElementById("pname").innerHTML = ""
    document.getElementById("pteam").innerHTML = ""
    document.getElementById("pnum").innerHTML = ""
    document.getElementById("ppos").innerHTML = ""
    document.getElementById('ppic').src='static/images/basketball.png'

    

}

function clearplayerdropdown()
{
    const playerInput = document.getElementById("player-input");
    playerInput.value = ""
    document.getElementById("pname").innerHTML = ""
    document.getElementById("pteam").innerHTML = ""
    document.getElementById("pnum").innerHTML = ""
    document.getElementById("ppos").innerHTML = ""
    document.getElementById('ppic').src='static/images/basketball.png'
}


function toggleSearch()
{
    $('.sidebar').toggleClass("open");
    //$('.search-btn').toggleClass("click");
}


function addStats()
{
    player_name = $("#player-input").val();

    $.get("/update_player_stats/" + player_name, function (dict) {

        console.log(dict)
        document.getElementById("gp").innerHTML = dict['games_played']
        document.getElementById("ast").innerHTML = dict['ast']
        document.getElementById("blk").innerHTML = dict['blk']
        document.getElementById("dreb").innerHTML = dict['dreb']
        document.getElementById("oreb").innerHTML = dict['oreb']
        document.getElementById("fg3pct").innerHTML = dict['fg3_pct']
        document.getElementById("fg3a").innerHTML = dict['fg3a']
        document.getElementById("fg3m").innerHTML = dict['fg3m']
        document.getElementById("fgpct").innerHTML = dict['fg_pct']
        document.getElementById("fga").innerHTML = dict['fga']
        document.getElementById("fgm").innerHTML = dict['fgm']
        document.getElementById("ftpct").innerHTML = dict['ft_pct']
        document.getElementById("ftm").innerHTML = dict['ftm']
        document.getElementById("fta").innerHTML = dict['fta']
        document.getElementById("mp").innerHTML = dict['min']
        document.getElementById("pf").innerHTML = dict['pf']
        document.getElementById("pts").innerHTML = dict['pts']
        document.getElementById("reb").innerHTML = dict['reb']
        document.getElementById("stl").innerHTML = dict['stl']
        document.getElementById("tu").innerHTML = dict['turnover']
      
        document.getElementById("pts1").innerHTML = dict['pts']
        document.getElementById("reb1").innerHTML = dict['reb']
        document.getElementById("ast1").innerHTML = dict['ast']

        

        
        
        
        // Load the Visualization API and the piechart package.
      google.charts.load('current', {'packages':['line']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.charts.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table, 
      // instantiates the pie chart, passes in the data and
      // draws it.
        function drawChart() {
                    var season=2020
            // Create the data table.
                    var data = new google.visualization.DataTable();
                    data.addColumn('string', 'Season'); //decimal?
                    data.addColumn('number', 'Points');
                    data.addColumn('number', 'Rebounds');
                    data.addColumn('number', 'Assists');

                    data.addRows([
                    ["2018", dict['ppg_2018'], dict['rpg_2018'], dict['apg_2018']],
                    ["2019", dict['ppg_2019'], dict['rpg_2019'], dict['apg_2019']],
                    ["2020", dict['ppg_2020'], dict['rpg_2020'], dict['apg_2020']]
                ]);

            // Set chart options
            var options = {
                height: 330,
                width: 700,
                hAxis: { textStyle: { color: '#FFF' } },
                vAxis: { textStyle: { color: '#FFF' }, viewWindow: { min: 0 }, gridlines: { color: 'transparent' }},
                legend: { position: 'left', textStyle: { color: 'white', fontSize: 16 } },
                backgroundColor: { fill: 'transparent' },
                chartArea: { backgroundColor: { fill: 'transparent',stroke: 'white', strokeWidth: 1 }},
            };

            // Instantiate and draw our chart, passing in some options.
            var chart = new google.charts.Line(document.getElementById('chart_div'));
            chart.draw(data, google.charts.Line.convertOptions(options));
    }
 
      
    });
    
   
}


  function checkIfImageExists(url, callback) {
    const img = new Image();

    img.src = url;

    if (img.complete) {
      callback(true);
    } else {
      img.onload = () => {
        callback(true);
      };
      
      img.onerror = () => {
        callback(false);
      };
    }
  }


$(document).ready(function () {
            
        var team_name = '';
        var player_name = '';
         var select = document.getElementById("players");

        $('#team-input').on('change', function () {
            console.log("Team Changed")
            team_name = $("#team-input").val();
            console.log(team_name)
            
            $('#players').children('option').remove();
            $.get("/players/"+team_name, function(dict) {
                
    
               var array = dict["players"]
               console.log(array)
        
                //$('#players-div').replaceWith(array)
                
        
                index=0;
                for (player in array) {
                    var opt = document.createElement("option");
                    opt.value = array[index];
                    opt.innerHTML = array[index]; // whatever property it has

                    // then append it to the select element
                    select.appendChild(opt);
                    index++;
                }

            });

        });
    
    
        
        
    $('#player-input').on('change', function () {
        player_name = $("#player-input").val();
        console.log("Player Changed")
        console.log(player_name)
        
        $.get("/update_player_info/" + player_name, function (dict) {
            console.log(dict)
            
            document.getElementById("pname").innerHTML = dict["name"]
            document.getElementById("pteam").innerHTML = dict["team"]
            if (dict["number"]!== null) {
                document.getElementById("pnum").innerHTML = "#"+dict["number"]
            }
            else {
                document.getElementById("pnum").innerHTML = ""
            }
            if (dict["position"]!== null) {
                document.getElementById("ppos").innerHTML = dict["position"]
            }
            else {
                document.getElementById("ppos").innerHTML = ""
            }
            if (dict["image link"]!== null) {
               document.getElementById('ppic').src=dict["image link"]
            }
            else {
                document.getElementById('ppic').src = 'static/images/basketball.png'
            }
        });

    });
    
 

    
            
})