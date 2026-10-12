
const API_URL = 'https://stock-screener-backend-okep.onrender.com';

export async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('access_token');

  const headers = {
    ...(options.body ? { 'Content-Type': 'application/json' } : {}),
    ...(options.headers || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    let errorMessage = 'Request failed';

    if (data?.detail) {
      if (Array.isArray(data.detail)) {
        errorMessage = data.detail
          .map((error) => {
            const field =
              error.loc
                ?.filter((item) => item !== 'body')
                .join('.') || 'field';

            return `${field}: ${error.msg}`;
          })
          .join(' | ');
      } else if (typeof data.detail === 'string') {
        errorMessage = data.detail;
      } else {
        errorMessage = JSON.stringify(data.detail);
      }
    } else if (data?.message) {
      errorMessage = data.message;
    }

    throw new Error(errorMessage);
  }

  return data;
}
