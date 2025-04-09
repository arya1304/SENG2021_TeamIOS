// register
document.getElementById('btn-register').addEventListener('click', async () => {
    const username = document.getElementById('register-name').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch("https://t6r6w5zni9.execute-api.us-east-1.amazonaws.com/v3/users/signUp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
        });

        if (!response.ok) {
            alert('Failed to register')
        }

        const data = await response.json();
        console.log("register response:", data);

        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
});

// login
document.getElementById('btn-login').addEventListener('click', async () => {
    const username = document.getElementById('login-name').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch("https://t6r6w5zni9.execute-api.us-east-1.amazonaws.com/v3/users/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
        });

        const data = await response.json();
        console.log("login response:", data);

        if (data.statusCode !== 200) {
            alert(data.body || "Login failed");
            return;
        }

        sessionStorage.setItem("token", data.token);
        showPage("main")
    } catch (err) {
        console.error(err.message);
        alert("An unexpected error occurred during login.");
    }
});

document.getElementById('btn-list-advice').addEventListener('click', async () => {    
    try {
        const token = sessionStorage.getItem("token");

        const response = await fetch("https://t6r6w5zni9.execute-api.us-east-1.amazonaws.com/v3/despatchAdvice", {
        method: "GET",
        headers: {
            Authorization: token
        }
        });

        if (!response.ok) {
            alert('Failed to get lists')
        }

        const data = await response.json();
        console.log(data.despatchAdvicesIDs);
        console.log("get list advices response:", data);

        const listContainer = document.getElementById("despatch-list");
        listContainer.innerHTML = "";

        const ids = data.despatchAdvices.despatchAdvicesIDs;

        ids.forEach((idText) => {
            const li = document.createElement("li");
            li.textContent = idText;
            listContainer.appendChild(li);
        });


        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
});


document.getElementById('btn-items').addEventListener('click', async() => {
    const despatchId = document.getElementById('items-id').value;
    
    try {
        const token = sessionStorage.getItem("token");
        
        const response = await fetch(`https://t6r6w5zni9.execute-api.us-east-1.amazonaws.com/v3/despatchAdvice/${despatchId}/items`, {
            method: "GET",
            headers: {
                Authorization: token
            }
        });
        
        if (response.status !== 200) {
            alert('Failed to get items')
            return;
        }
        
        const data = await response.json();
        console.log("user response:", data);

        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(data.Items, "application/xml");
        
        const list = document.getElementById("items-list");
        list.innerHTML = ""; // 기존 내용 초기화

        const item = xmlDoc.getElementsByTagName("Item")[0];

        if (item) {
            const name = item.getElementsByTagName("cbc:Name")[0]?.textContent || "N/A";
            const description = item.getElementsByTagName("cbc:Description")[0]?.textContent || "N/A";
            const buyerID = item.getElementsByTagName("cbc:ID")[0]?.textContent || "N/A";
            const sellerID = item.getElementsByTagName("cac:SellersItemIdentification")[0]?.getElementsByTagName("cbc:ID")[0]?.textContent || "N/A";
            const lotNumber = item.getElementsByTagName("cbc:LotNumberID")[0]?.textContent || "N/A";
            const expiryDate = item.getElementsByTagName("cbc:ExpiryDate")[0]?.textContent || "N/A";

            const details = `
                <li><strong>Name:</strong> ${name}</li>
                <li><strong>Description:</strong> ${description}</li>
                <li><strong>Buyer ID:</strong> ${buyerID}</li>
                <li><strong>Seller ID:</strong> ${sellerID}</li>
                <li><strong>Lot Number:</strong> ${lotNumber}</li>
                <li><strong>Expiry Date:</strong> ${expiryDate}</li>
            `;
            list.innerHTML = details;
        } else {
            list.innerHTML = "<li>No item found.</li>";
        }

        showPage("main");
    } catch (err) {
        console.error(err.message);
    }
})

document.getElementById('btn-delete-user').addEventListener('click', async() => {
    const id = document.getElementById('user-id').value;
    
    try {
        const token = sessionStorage.getItem("token");
        
        const response = await fetch(`https://seapi.vercel.app/v1/user/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            alert('Failed to delete user')
        }
        
        const data = await response.json();
        console.log("user response:", data);
        
        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
})

document.getElementById('btn-get-user').addEventListener('click', async() => {
    const id = document.getElementById('user-id').value;

    try {
        const token = sessionStorage.getItem("token");

        const response = await fetch(`https://seapi.vercel.app/v1/user/${id}`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
    });

        if (!response.ok) {
            alert('Failed to get user')
        }

        const data = await response.json();
        console.log("user response:", data);

        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
})

const callProtectedAPI = async () => {
    const token = localStorage.getItem("token");
  
    const res = await fetch("https://seapi.vercel.app/v1/some/protected/endpoint", {
        method: "GET",
        headers: {
        Authorization: `Bearer ${token}`
      }
    });
  
    const data = await res.json();
};

const showPage = (pageName) => {
    const pages = document.querySelectorAll('.page');
    for (const page of pages) {
        page.classList.add('hide');
    }
    document.getElementById(`page-${pageName}`).classList.remove('hide');
}

document.addEventListener("DOMContentLoaded", () => {
    showPage("landing");
});