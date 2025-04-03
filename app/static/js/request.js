function loginRequest(url, method, data) {
    return request(getApiBase() + url, method, data)
}

function getDashboardInfo(url, method, data) {
    return request(getApiBase() + url, method, data, {'Authorization': `Bearer ${localStorage.getItem('Authorization')}`})
}