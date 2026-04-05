const baseUrl = "https://API_KEY.execute-api.ap-northeast-1.amazonaws.com";

  fetch(baseUrl + "/csv")
  .then(response => response.text())
  .then(csvText => {
    const lines = csvText.trim().split("\n");
    const container = document.getElementById("list");

    lines.forEach(line => {
      const columns = line.split(",");

      const row = document.createElement("div");
      row.className = "row";
      row.style.backgroundColor = "#FFFFFF"

      for (let i = 0; i < 5; i++) {
        const span = document.createElement("span");
        span.className = "span2";
        span.textContent = columns[i];
        row.appendChild(span);
      }

      const button = document.createElement("button");
      if (Number(columns[4]) < 12) {
        button.style.backgroundColor = 'red';
        button.textContent = "少頭数";
      } else {
        button.textContent = "反映";
      }

      row.appendChild(button);

      function makeSpan(txt) {
        const newSpan = document.createElement("span");
        newSpan.className = "span3"
        newSpan.textContent = txt;
        row.appendChild(newSpan);
        return newSpan;
      }

      const spanResult1 = makeSpan("Result1");
      const spanResult2 = makeSpan("Result2");
      const spanExpDev1 = makeSpan("ExpDev1");
      const spanExpDev2 = makeSpan("ExpDev2");
      const spanGetTime = makeSpan("getTime");

      const button2 = document.createElement("button");
      button2.textContent = "check";

      row.appendChild(button2);

      button.onclick = async () => {
        button.disabled = true; // 待機状態（無効化）
        button.innerText = '待機';

        const payload = {
          col1: columns[0],
          col2: columns[1],
          col3: columns[2]
        };

        try {
          const response = await fetch(baseUrl + "/getExpDev", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
          });

          const result = await response.json();

          spanResult1.textContent = result.data1;
          spanResult2.textContent = result.data2;

          spanExpDev1.textContent = result.data3;
          spanExpDev2.textContent = result.data4;

          const exp1 = Number(spanExpDev1.textContent)
          const exp2 = Number(spanExpDev2.textContent)

          spanExpDev1.style.backgroundColor = '';
          spanExpDev2.style.backgroundColor = '';

          if (exp1 > 10000 && exp2 > 10000) {
            if (exp1 > exp2) {
              spanExpDev1.style.backgroundColor = 'green';
            } else if (exp1 < exp2) {
              spanExpDev2.style.backgroundColor = 'red';
            }
          }

          spanGetTime.textContent = result.data5;

          button.disabled = false;
          button.innerText = '反映';
        } catch (error) {
          alert("送信失敗: " + error);

          button.disabled = false;
          button.innerText = '反映';
        }
      };

      button2.onclick = async () => {
        if (button2.textContent == "check") {
          button2.textContent = "checked"
          row.style.backgroundColor = "#2ff016";

          const [hour, minute] = columns[3].split(":").map(Number);

          const now = new Date();
          const target = new Date();

          target.setHours(hour);
          target.setMinutes(minute - 10);
          target.setSeconds(0);

          const diff = target - now;

          alert('タイマーをセットしました。');

          setTimeout(() => {
            alert("10分前です！");
            const audio = new Audio("https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg");
            audio.play();
          }, diff);
        } else if (button2.textContent == "checked") {
          button2.textContent = "check"
          row.style.backgroundColor = "#FFFFFF";
        }
      };

      container.appendChild(row);
    });
  });