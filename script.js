// เปิดใช้งานปุ่มเมื่อเลือกไฟล์
document.getElementById('cameraInput').addEventListener('change', function(e) {
  const detectBtn = document.getElementById('detectBtn');
  const fileName = document.getElementById('fileName');
  
  if (e.target.files.length > 0) {
    detectBtn.disabled = false;
    fileName.textContent = `เลือกไฟล์: ${e.target.files[0].name}`;
    fileName.style.display = 'block';
  } else {
    detectBtn.disabled = true;
    fileName.style.display = 'none';
  }
});

function uploadImage() {
  const input = document.getElementById('cameraInput');
  const resultText = document.getElementById('resultText');
  const resultImage = document.getElementById('resultImage');
  const loadingSpinner = document.getElementById('loadingSpinner');
  const btnText = document.getElementById('btnText');
  const detectBtn = document.getElementById('detectBtn');

  if (input.files.length === 0) {
    alert('กรุณาเลือกไฟล์');
    return;
  }

  // แสดงสถานะกำลังโหลด
  detectBtn.disabled = true;
  loadingSpinner.style.display = 'inline-block';
  btnText.textContent = 'กำลังตรวจจับ...';
  resultText.textContent = 'กำลังประมวลผลภาพ กรุณารอสักครู่...';
  resultText.className = 'loading';
  resultImage.style.display = 'none';
  resultImage.classList.remove('show');

  const file = input.files[0]; 
  const formData = new FormData();
  formData.append('image', file);

  const apiUrl = 'http://127.0.0.1:3000/detect';

  fetch(apiUrl, {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    if (data.image) {
      // แสดงผลลัพธ์สำเร็จ
      let resultMessage = `🎯 ตรวจพบไม้สี ${data.count} ชิ้น`;
      
      // แสดงรายละเอียดตามสีถ้ามี
      if (data.color_breakdown) {
        const colorDetails = Object.entries(data.color_breakdown)
          .map(([color, count]) => `${color}: ${count}`)
          .join(', ');
        resultMessage += `\n(${colorDetails})`;
      }
      
      resultText.textContent = resultMessage;
      resultText.className = 'success';
      resultImage.src = `data:image/jpeg;base64,${data.image}`;
      resultImage.style.display = 'block';
      resultImage.classList.add('show');
    } else {
      throw new Error(data.error || 'ไม่ได้รับข้อมูลภาพจากเซิร์ฟเวอร์');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    resultText.textContent = `❌ เกิดข้อผิดพลาด: ${error.message}`;
    resultText.className = 'error';
    resultImage.style.display = 'none';
    resultImage.classList.remove('show');
  })
  .finally(() => {
    // รีเซ็ตสถานะปุ่ม
    detectBtn.disabled = false;
    loadingSpinner.style.display = 'none';
    btnText.textContent = '🔍 เริ่มตรวจจับไม้';
  });
}