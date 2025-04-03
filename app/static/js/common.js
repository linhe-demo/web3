function getApiBase() {
    return "";
}

function showAlert(type, message) {
    const $alert = $(`
      <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    `);
    $('#loginForm').prepend($alert);
    setTimeout(() => $alert.alert('close'), 5000);
}

/**
 * 封装AJAX请求
 * @param {string} url 请求地址
 * @param {string} method HTTP方法 (GET/POST/PUT/DELETE等)
 * @param {object} params 请求参数
 * @param {object} headers 自定义请求头
 * @returns {Promise} 返回Promise对象
 */
function request(url, method = 'GET', params = null, headers = {}) {
    return new Promise((resolve, reject) => {
        // 基本配置
        const config = {
            url: url,
            type: method.toUpperCase(),
            dataType: 'json',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                ...headers  // 合并自定义头
            },
            success: function(response) {
                if (response.code === 200) {
                    resolve(response.data);
                } else {
                    const errorMsg = response?.message || '请求失败';
                    console.log(22)
                    showError(errorMsg);  // 显示错误提示
                    reject(errorMsg);
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                const errorMsg = getErrorMessage(xhr, textStatus);
                toastr.error("登录令牌失效，请重试！")
                if (xhr.status === 422) {
                    window.location.href = '/';
                    return
                }
                reject(errorMsg);
            }
        };

        // 参数处理
        if (params) {
            if (config.type === 'GET') {
                config.data = params;
            } else {
                config.contentType = 'application/json';
                config.data = JSON.stringify(params);
            }
        }

        // 发送请求
        $.ajax(config);
    });
}

/**
 * 获取友好的错误信息
 */
function getErrorMessage(xhr, textStatus) {
    // 超时
    if (textStatus === 'timeout') {
        return '请求超时，请稍后重试';
    }
    // 网络错误
    if (textStatus === 'error' && !xhr.responseText) {
        return '网络连接失败';
    }
    // 尝试解析响应错误
    try {
        const response = xhr.responseJSON;
        if (response && response.message) {
            return response.message;
        }
    } catch (e) {
        console.error('解析错误信息失败:', e);
    }
    // 默认错误
    return xhr.statusText || `请求失败 (${xhr.status})`;
}

/**
 * 显示错误提示
 * (使用Toastr或降级到alert)
 */
function showError(message) {
    if (typeof toastr !== 'undefined') {
        toastr.error(message);
    } else {
        alert(message);
    }
}