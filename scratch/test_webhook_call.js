const axios = require('axios');

(async () => {
  try {
    const res = await axios.post(
      'http://localhost:3000/webhook',
      'Body=What+are+your+store+hours%3F&From=whatsapp%3A%2B1234567890',
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
    console.log('HTTP STATUS:', res.status);
    console.log('RESPONSE DATA:', res.data);
  } catch (err) {
    console.error('ERROR:', err.response ? err.response.data : err.message);
  }
})();
