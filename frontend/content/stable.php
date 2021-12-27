<style scoped>
    .grid {
        position: fixed;
        left: 8px;
        right: 10px;
        top: 95px;
        bottom: 40px;
        overflow-y: auto;
        display: grid;
        grid-template-columns: 1fr 2.5fr;
        grid-gap: 10px;
    }

    .nextup {
        grid-column: 1/2;
        grid-row: 1/2;
        //height: auto;
        //width: 100%;
    }

    .stats {
        grid-column: 1/2;
        grid-row: 2/3;
        //height: 100%;
        //width: 100%;
    }

    .map {
        grid-column: 2/2;
        grid-row: 1/3;
	//height: 100%;
	//width: 100%;
    }

    #nextupdiv {
        margin: 5px;
//        overflow-y:scroll;
    }

    #nextupdiv p {
        display:inline;
        font-size: 1.2em
    }

    #statsdiv {
        margin: 5px;
//        overflow-y:scroll;
    }

    #statsdiv p {
        display:inline;
        font-size: 1.2em
    }

    #leafletmap {
        height: 100%;
        width: 100%;
    }
</style>

<div class="grid">
  <div class="nextup" style="border: green 1px solid;">
    <div id="nextupdiv">
      <p>Landing Planes:</p>
      </br>
      <table cellspacing="20">
        <tbody>
          <tr>
            <td>1.</td>
            <td><img id="image1" src="images/planes/unknown.png" width="80" height="60"></td>
            <td id="name1">-</td>
            <td id="height1">?m</td>
            <td id="time1">?s</td>
          </tr>
          <tr>
            <td>2.</td>
            <td><img id="image2" src="images/planes/unknown.png" width="80" height="60"></td>
            <td id="name2">-</td>
            <td id="height2">?m</td>
            <td id="time2">?s</td>
          </tr>
          <tr>
            <td>3.</td>
            <td><img id="image3" src="images/planes/unknown.png" width="80" height="60"></td>
            <td id="name3">-</td>
            <td id="height3">?m</td>
            <td id="time3">?s</td>
          </tr>
        </tbody>
      </table>
      <script src="scripts/nextup.js"></script>
    </div>
  </div>

  <div class="stats" style="border: green 1px solid;">
    <div id="statsdiv">
      <p>Statistik:</p>
      <table cellspacing="5">
        <tr>
          <td>Flugzeuge in der Luft:</td>
          <td>5</td>
        </tr>
        <tr>
          <td>Flugzeuge am Boden:</td>
          <td>2</td>
        </tr>
        <tr>
          <td>Gesamt Starts:</td>
          <td>25</td>
        </tr>
      </table>
    </div>
  </div>

  <div class="map" style="border: green 1px solid;">
    <div id="leafletmap"></div>
    <script src="scripts/mapscript.js"></script>
  </div>
</div>

<script src="scripts/loader.js"></script>
