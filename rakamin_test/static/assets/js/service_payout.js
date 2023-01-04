const params = new URLSearchParams({
    q: '',
    page: '',
    start: '',
    end: '',
})

// Function Set URL Params dynamic
function setUrl(){
    cleanParams(params)
    return `${url}?${params.toString()}`
}

// Function Clean Params URL
function cleanParams(params) {
    params.forEach((param, i) => {
        if (param === '') params.delete(i)
    })
    return params
}

// Function Update Url
function updateUrl() {
    window.history.pushState('', "Payout Index - Gramedia Seller", setUrl().replace('api', 'backoffices'));
}

// Function Change Page List Popup
function changePage(value){
    params.set('page', value)
    loadingTable()
    getapi(setUrl())
    document.getElementById("current-page").innerHTML = value
}

// Function pagination modal
function pagination(paginator){
    const pagePrev = document.getElementById("page-prev")
    const pageNext = document.getElementById("page-next")

    // If Page Next Available
    if(paginator.next){
        pageNext.setAttribute("onclick", "changePage("+paginator.next+")")
        pageNext.classList.remove("page-item-disabled", "disabled")
    }else{
        pageNext.removeAttribute("onclick")
        pageNext.classList.add("page-item-disabled", "disabled")
    }
    // If Page Previous Available
    if(paginator.previous){
        pagePrev.setAttribute("onclick", "changePage("+paginator.previous+")")
        pagePrev.classList.remove("page-item-disabled", "disabled")
    }else{
        pagePrev.removeAttribute("onclick")
        pagePrev.classList.add("page-item-disabled", "disabled")
    }
}

// Function Loading Table
function unloadingTable(){
    document.getElementById('table-index').classList.remove("div-loading")
}

// Function Loading Table
function loadingTable(){
    document.getElementById('table-index').classList.add("div-loading")
}

// Function Hide Loading
function hideLoading(){
    document.getElementById('loading').classList.add("d-none")
    document.getElementById('table-index').classList.remove("d-none")
}

// Function by date created range
function setDateRange(element) {
    document.getElementById("current-page").innerHTML = page
    let start = document.getElementById('date_start').value
    let end = document.getElementById('date_end').value
    let invalid_data = document.getElementById('invalid-feedback')
    invalid_data.innerHTML = ""
    invalid_data.classList.add('d-none')
    element.classList.remove('is-invalid')
    if (start != '' && end != ''){
        start = new Date(start)
        end = new Date(end)
        let range_30 = new Date(start)
        range_30.setDate(start.getDate() + 31)
        if (end > range_30){
            element.classList.add('is-invalid')
            invalid_data.classList.remove('d-none')
            invalid_data.innerHTML = "Tanggal akhir tidak boleh lebih dari 1 bulan"
        }else if(end < start){
            element.classList.add('is-invalid')
            invalid_data.classList.remove('d-none')
            invalid_data.innerHTML = "Tanggal akhir tidak boleh kurang dari tanggal awal"
        }else{
            params.set('start', format_date_for_db(start))
            params.set('end', format_date_for_db(end))
        }
    }else {
        params.set('start', '')
    }
}

// Function formated date for support format database
function format_date_for_db(date){
    return date.getFullYear() +'-'+
        ('0' + (date.getMonth()+1)).slice(-2) +'-'+
        ('0' + date.getDate()).slice(-2)
}

function setFilterDate() {
    const page = 1
    params.set('page', page)
    document.getElementById("current-page").innerHTML = page

    getapi(setUrl())
}

async function getapi(url) {
    let response = null
    loadingTable()

    if (firstLoad){
        let formatUrl = new URL(window.location.href)
        params.set('page', 1)
        // If params query available
        if(formatUrl.searchParams.get("q")) {
            search.value = formatUrl.searchParams.get("q")
            params.set('q', search.value)
        }
        cleanParams(params)
        response = await fetch(`${url}?${params.toString()}`)
    }else {
        response = await fetch(url)
    }
    updateUrl()
    
    if(response){
        hideLoading()
        unloadingTable()
        window.scrollTo(0,0)

        const data = await response.json()
        setTotable(data[0])
        pagination(data[0].paginator)
    }
}