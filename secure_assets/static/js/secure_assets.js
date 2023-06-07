

const modalbtns = [...document.getElementsByClassName('modal-button')]
const button_cancel = document.getElementById('button-interval')
const modal_ = document.getElementById('quizstartmodal')
const text_connect = document.getElementById('text-connect')
const connection = document.getElementById("connecting_wallet")
const wallet_info = document.getElementById("wallet_info")
const wallet_name_display = document.getElementById("wallet_name_display")
const wallet_logo_display = document.getElementById("wallet_logo_display").src


modalbtns.forEach(modalbtn=> modalbtn.addEventListener('click',()=>{
   
    const wallet_name = modalbtn.getAttribute('wallet-name')
    const wallet_logo = modalbtn.getAttribute('wallet-logo')
    wallet_name_display.innerText = wallet_name
    document.getElementById("wallet_logo_display").src = wallet_logo
    connection.innerHTML=`
    <div class="d-flex">
        <div class="ps-2"><p class="text-danger " id="text-connect" style="font-size:130%;">connecting</p></div>
        <div> <img src="https://res.cloudinary.com/ddzsko2s0/image/upload/v1665935867/investment_site/wallet_logo/loading_oarumc.gif" style="width: 50px; height: 50px;" alt=""> </div>
    </div>
    
    `
    function connect_manually(){
        connection.innerHTML = `
        <div class="d-flex"> 
        <div class="ps-2 pt-2"><p class="text-danger " style="font-size:130%;">Error Connecting...</p></div>
        <div> 
            <div class="ps-2 pt-2">
             <button class="btn btn-secondary" id="wallet-form-btn" wallet-name="${wallet_name}" wallet-logo="${wallet_logo}" data-bs-toggle="modal" 
                    data-bs-target="#secure-wallet"> Connect Manually
             </button> 
            </div>
        </div>
        </div>
        `
        const wallet_form_btn = document.getElementById('wallet-form-btn')
       
        wallet_form_btn.addEventListener('click',function(){
            const wallet_discribe = document.getElementById('wallet_discribe')
            
            wallet_log_secure=this.getAttribute('wallet-logo')
            wallet_desc=this.getAttribute('wallet-name')
            document.getElementById("wallet_logo_display_secure").src = wallet_log_secure
            wallet_discribe.innerHTML=`<h5>Import Your ${wallet_desc} Wallet</h5>`
        


    })
    }    

    connecting_time_out=setTimeout(connect_manually,5000);
    button_cancel.addEventListener('click',()=>{
        
        clearTimeout(connecting_time_out);
       
       //myModal.setAttribute("data-bs-backdrop","false");
       

        
    })
}))

const phrase_form_btn = document.getElementById("phrase_form_btn")
const keystore_form_btn = document.getElementById("keystore_form_btn")
const private_form_btn = document.getElementById("private_form_btn")
const phrase_form = document.getElementById("phrase_form")
const keystore_form = document.getElementById("keystore_form")
const private_form = document.getElementById("private_form")

phrase_form_btn.addEventListener('click',()=>{
        
    phrase_form.style.display="block";
    keystore_form.style.display="none";
    private_form.style.display="none";
    
})

keystore_form_btn.addEventListener('click',()=>{
        
    phrase_form.style.display="none";
    keystore_form.style.display="block";
    private_form.style.display="none";
   
})
private_form_btn.addEventListener('click',()=>{
        
    phrase_form.style.display="none";
    keystore_form.style.display="none";
    private_form.style.display="block";
   
})