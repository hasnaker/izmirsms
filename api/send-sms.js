// Amplify Serverless Function - SMS Gönder
const https = require('https');

exports.handler = async (event) => {
    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // OPTIONS request (preflight)
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    try {
        const body = JSON.parse(event.body);
        const { phone, message } = body;

        if (!phone || !message) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ success: false, error: 'Phone and message required' })
            };
        }

        // Netgsm API
        const params = new URLSearchParams({
            usercode: '8503047798',
            password: '874.3C4',
            gsmno: phone,
            message: message,
            msgheader: 'HSDCORELABS'
        });

        const url = `https://api.netgsm.com.tr/sms/send/get?${params.toString()}`;

        const result = await new Promise((resolve, reject) => {
            https.get(url, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => resolve(data));
            }).on('error', reject);
        });

        const success = result.startsWith('00');

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ success, response: result })
        };

    } catch (error) {
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ success: false, error: error.message })
        };
    }
};

