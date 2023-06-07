
const investment_td = [...document.getElementsByClassName('investments')]
const get_the_date = document.getElementById('dates')
const url = window.location.href
const csrf = document.getElementsByName("csrfmiddlewaretoken")

const profit_result = {'csrfmiddlewaretoken': csrf[0].value};
const display_result = {}
investment_td.forEach(get_profit);


function get_profit(item){
    
    const investment_id = item.getAttribute('investment-id')
    const investment_ammount = item.getAttribute('investment-amount')
    const investment_percent = item.getAttribute('investment-percent')
    const investment_date_of_trade = item.getAttribute('investment-date_of_trade')
    const investment_date_of = item.getAttribute('investment-date_of')
    const investment_trade_mode = item.getAttribute('investment-trade_mode')
    const investment_time = item.getAttribute('investment-time')
    const todays_date = get_the_date.getAttribute('today-date')

    const strip_out_microsec_for_today_date = todays_date.split(".")
    let strip_out_microsec_for_trading_date_end = investment_date_of_trade.split("+")
    strip_out_microsec_for_trading_date_end = strip_out_microsec_for_trading_date_end[0].split(".")
    
    let profit_amount = (parseInt(investment_percent)/100) * parseInt(investment_ammount)
    
    if(investment_trade_mode=="running"){
        const total_time_s = parseInt(investment_time) * 60 * 60
        const trade_date = Date.parse(strip_out_microsec_for_trading_date_end[0])
        const date_now = Date.parse(strip_out_microsec_for_today_date[0])
    
        const time_of_trade = (trade_date - date_now)/1000
       
        const profit_per = (time_of_trade*profit_amount) / total_time_s
        const the_profit_per = Math.round((profit_amount - profit_per) * 100)/100

        profit_result[investment_id] = the_profit_per
        display_result[investment_id] = the_profit_per

        
        
    }
}


$.ajax({
    type: "POST",
    url: `${url}save_prof/`,
    data: profit_result,
    success: function (result) {
        
        for (const[key, value] of Object.entries(result.results)){
            document.getElementById(`profit${key}`).innerText = `${value}$`
        }
    }
  });