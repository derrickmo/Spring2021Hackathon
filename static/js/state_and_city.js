var states = Object();
states['AL'] = 'Alexander City|Andalusia|Anniston|Athens|Atmore|Auburn|Bessemer|Birmingham|Chickasaw';
states['AK'] = 'Anchorage|Cordova|Fairbanks|Haines|Homer|Juneau|Ketchikan';
states['AZ'] = 'Ajo|Avondale|Bisbee|Casa Grande|Chandler|Clifton|Douglas|Flagstaff|Florence|Gila Bend|Glendale|Globe|Kingman|Lake Havasu City|Mesa|Nogales|Oraibi|Phoenix|Prescott|Scottsdale|Sierra Vista|Tempe|Tombstone|Tucson|Walpi|Window Rock|Winslow|Yuma';
states['AR'] = 'Arkansas|Arkadelphia|Arkansas Post|Batesville|Benton|Blytheville|Camden|Conway|Crossett|El Dorado|Fayetteville|Forrest City|Fort Smith|Harrison'
states['CA'] = 'Alameda|Belmont|Berkeley|Beverly Hills|Calexico|Carmel|Chico|Chula Vista|Claremont|Costa Mesa|Culver City|Daly City|Davis|Fremont|Los Angeles|Mountain View|Napa|Oakland|Palm Springs|Palo Alto|Sacramento|San Francisco|San Gabriel|San Jose'
states['PA'] = 'Philadelphia'
function set_state(s)
{
  
  const state = states[s].split("|");
  var toAdd = document.getElementById("city");
  $(toAdd).empty();


  var l = state.length;
  for (var i = 0; i < l; i++){
  	var option = document.createElement("option");
	option.text = state[i];
	option.value = state[i];
	toAdd.appendChild(option);
  }
    // document.getElementById("city").write('<option value="' + city + '">' + city + '</option>');
}
