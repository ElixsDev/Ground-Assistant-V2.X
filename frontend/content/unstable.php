<style scoped>
    .grid {
        position: fixed;
        left: 8px;
        right: 10px;
        top: 95px;
        bottom: 40px;
        display: grid;
        grid-template-columns: 1fr 2.5fr;
        grid-gap: 10px;
    }

    .nextup {
        grid-column: 1/2;
        grid-row: 1/2;
        height: 100%;
        width: 100%;
    }

    .stats {
        grid-column: 1/2;
        grid-row: 2/3;
        height: 100%;
        width: 100%;
    }

    .map {
        grid-column: 2/2;
        grid-row: 1/3;
	height: 100%;
	width: 100%;
    }

    #leafletmap {
        height: 100%;
        width: 100%;
    }
</style>

<div class="grid">
  <div class="nextup" style="border: green 1px solid;">
    Next Up
  </div>

  <div class="stats" style="border: green 1px solid;">
    Stats
  </div>

  <div class="map" style="border: green 1px solid;">
    <div id="leafletmap"></div>
    <script src="content/mapscript.js"></script>
  </div>
</div>
