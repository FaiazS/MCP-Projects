from enum import Enum

css = """

.postive-pnl{

    color: green !important;

    font-weight:bold;

}

.positive-bg {

    background-color: green !important;

    font-weight: bold;
    
    }

.negative-bg {

    background-color: red !important;

    font-weight: bold;

    }

.negative-pnl {

    color: red !important;

    font-weight: bold;
    
    }


.dataframe-fix-small .table-wrap{

    min-height: 150px

    max-height: 150px;

}


.dataframe-fix .table-wrap{

    min-height: 200px;

    max-height: 200px;

}

footer{display: none !important;}

"""


js = """

function refresh(){

     const url = new URL(windows.location);

     if(url.searchParams.get('__theme') != 'dark'){
     
     url.searchParams.set('__theme', 'dark');

     windows.location.href = url.href;
     
     }
}

"""

class Color(Enum):

    RED = "#dd0000"

    GREEN = "#00dd00"

    YELLOW = "#dddd00"

    BLUE =  "#0000ee"

    MAGENTA = "#aa00dd"

    CYAN =  "#00dddd"

    WHITE =  "#87CEEB"