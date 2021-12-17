// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"

console.log('HALO')

function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        items.sort(function(a, b) {
          var desA = a.Description.toUpperCase()
          var desB = b.Description.toUpperCase()
          if (desA < desB) {
            return -1;
          }
          if (desA > desB) {
            return 1;
          }
          return 0;
        })
    } else {
        items.sort(function(a, b) {
          var desA = a.Description.toUpperCase()
          var desB = b.Description.toUpperCase()
          if (desA < desB) {
            return 1;
          }
          if (desA > desB) {
            return -1;
          }
          return 0;
        })
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
// var items = document.getElementById('bonus_questions')
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)
    let filteredList = []
    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    for (let i=0; i<items.length; i++) {
        if (items[i]['Title'].includes(filterValue)) {
            filteredList.push(items[i])

        }

        else if (filterValue.slice(0, 13) == "!Description:" && !items[i]['Description'].includes(filterValue.slice(13, filterValue.length))) {
            filteredList.push(items[i])
        }

        else if (filterValue[0] == "!" && !filterValue.includes('Description') && !items[i]['Title'].includes(filterValue.slice(1, filterValue.length))) {
            filteredList.push(items[i])
        }

        else if (filterValue.slice(0, 12) == "Description:" && items[i]['Description'].includes(filterValue.slice(12, filterValue.length))) {
            filteredList.push(items[i])
        }




    }

    return filteredList
}

function toggleTheme() {
    console.log("toggle theme")
    var element = document.body;
    element.classList.toggle("dark-mode");
    element.style.backgroundColor = "black";
    element.style.color ="white";
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}