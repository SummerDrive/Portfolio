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

            for (let i = 0; i < 5; i++) {
              const span = document.createElement("span");
              span.className = "span2";
              span.textContent = columns[i];
              row.appendChild(span);
            }

            const button = document.createElement("button");
            if (Number(columns[4]) < 12) {
              button.style.backgroundColor = 'red';
              button.textContent = "�???��??";
            } else {
              button.textContent = "??????";
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

            button.onclick = async () => {
              button.disabled = true; // �?�???��??�???��?��??�?
              button.innerText = '�?�?';

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

                spanGetTime.textContent = result.data5;

                button.disabled = false;
                button.innerText = '??????';
              } catch (error) {
                alert("???信失???: " + error);

                button.disabled = false;
                button.innerText = '??????';
              }
            };

            // row.appendChild(button);

            container.appendChild(row);
          });
        });