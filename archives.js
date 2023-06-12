



// const generateprn = document.getElementById('generate_prn');
// generateprn.addEventListener("click", async function generatePaymentRegistrationNumber(e){

//    const principle_licence_certificate_number  = document.getElementById('principle_licence_certificate_number');
//    const purpose_of_application = document.getElementById('purpose_of_application').value
//    const generate_prn  = document.getElementById('generate_prn').value
//    const prn  = document.getElementById('prn').value
//    const error_code  = document.getElementById('error_code').value
//    const error_desc  = document.getElementById('error_desc').value
//    const payment_expiry_date  = document.getElementById('payment_expiry_date').value
//    const search_code  = document.getElementById('search_code').value
//    const tin = document.getElementById('tin').value
//    const application_fee = document.getElementById("application_fee").value
//    const licence_fee = document.getElementById("licence_fee").value
//    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//    const application_fee_url = "{% url 'payments:get_prn_application_fee' %}"
//    const licence_fee_url = "{% url 'payments:get_prn_licence_fee' %}"

   
//    const ura_payload = JSON.stringify({
//       "application_fee" : application_fee,
//       "tin" : tin,
//    })

//    if( tin === ''){
//       Swal.fire({
//             icon: 'error',
//             title: 'Error',
//             text: 'TIN field can not be empty',
//             showConfirmButton: true,
//       })

//       document.getElementById("generate_prn").checked = false;

//    }


//    if(generateprn.checked == true){
//       console.log(purpose_of_application)

//       if(purpose_of_application == "Renewal"){
//          // licence fees

//          $.ajax({
//                url: licence_fee_url, 
//                type: "post",
//                data: {
//                   "licence_fee": licence_fee,
//                   "tin": tin,
//                },
//                dataType: "json",
//                headers: {'X-CSRFToken': csrftoken },
//                mode: 'same-origin',  
//                beforeSend: function () {
                  
//                    $('#spinner').show();
//                    $("#loading").addClass("loading")
                   
//                },
               
//                success: function (ura_response) {
                  
//                   const response = ura_response
//                   let val = response[ Object.keys( response )[ 0 ] ]

//                   if( Object.keys( val )[ 0 ] === "GetPRNResult" ) {
                     
//                      console.log( '1',val[ 'GetPRNResult' ] )

//                      tin_response = {
//                         'status': response.GetPRNResponse.GetPRNResult.ErrorDesc,
//                         'prn': response.GetPRNResponse.GetPRNResult.PRN,
//                         'error_code': response.GetPRNResponse.GetPRNResult.ErrorCode,
//                         'error_desc': response.GetPRNResponse.GetPRNResult.ErrorDesc,
//                         'payment_expiry_date': response.GetPRNResponse.GetPRNResult.ExpiryDate,
//                         'search_code': response.GetPRNResponse.GetPRNResult.SearchCode
//                      }
//                      console.log(tin_response)

//                      if(tin_response.status === "SUCCESS"){
//                         $("#prn").val(tin_response.prn)
//                         $("#error_code").val(tin_response.error_code)
//                         $("#rror_desc").val(tin_response.error_desc)
//                         $("#payment_expiry_date").val(tin_response.payment_expiry_date)
//                         $("#search_code").val(tin_response.search_code)
//                         $('#prnError').html('');
//                         console.log("now ")

                        

//                      } else if (tin_response.status === "INVALID TIN") {
//                            $("#tin").val('');
//                            $('#gernerate_prn').prop('checked', false)
//                            $("#prn").val('');
//                            swal.fire(status);
//                            $('.prnError').html('');
//                      } else if(tin_response.status === "Invalid Length of TIN Entered, please try again"){
//                            swal.fire(tin_response.status);
//                            $("#prn").val("");
//                            $("#error_code").val("");
//                            $("#error_desc").val("");
//                            $("#payment_expiry_date").val("");
//                            $("#search_code").val("");
//                            // $("<i class='tSx' class='green circular check mark icon'></i>" ).appendTo($("#Prn").parent());
//                            $('.prnError').html('');
//                            console.log("invalid tin number");
//                      } else{
//                            $("#prn").val("");
//                            $("#error_code").val("");
//                            $("#error_desc").val("");
//                            $("#payment_expiry_date").val("");
//                            $("#search_code").val("");
//                            $("#tSx").remove();
//                            $("<i id='tSx' class='red circular exclamation triangle icon'></i>").appendTo($("#Prn").parent());
//                            $('.prnError ').html("Failed to generate PRN");
//                            console.log("failed to generate PRN");

//                      }
                     
//                   } 
//                   else {
//                         console.log( '2', val )
                        
//                         tin_response = {
//                            'status': val.ErrorDesc,
//                            'prn': val.PRN,
//                            'ErrorCode': val.ErrorCode,
//                            'ErrorDesc': val.ErrorDesc,
//                            'ExpiryDate': val.ExpiryDate,
//                            'SearchCode': val.SearchCode
//                         }
//                         console.log(tin_response)

//                         if(tin_response.status === "SUCCESS"){
//                            $("#prn").val(tin_response.prn)
//                            $("#error_code").val(tin_response.ErrorCode)
//                            $("#error_desc").val(tin_response.ErrorDesc)
//                            $("#payment_expiry_date").val(tin_response.ExpiryDate)
//                            $("#search_code").val(tin_response.SearchCode)
//                            $('.prnError').html('');

//                         } else if (tin_response.status === "INVALID TIN") {
//                               $("#tin").val('');
//                               $('#gernerate_prn').prop('checked', false)
//                               $("#prn").val('');
//                               swal.fire(status);
//                               $('.prnError').html('');
//                         } else if(tin_response.status === "Invalid Length of TIN Entered, please try again"){
//                               swal.fire(tin_response.status);
//                               $("#prn").val("");
//                               $("#error_code").val("");
//                               $("#error_desc").val("");
//                               $("#payment_expiry_date").val("");
//                               $("#search_code").val("");
//                               // $("<i class='tSx' class='green circular check mark icon'></i>" ).appendTo($("#Prn").parent());
//                               $('.prnError').html('');
//                               console.log("invalid tin number");
//                         } else{
//                               $("#prn").val("");
//                               $("#error_code").val("");
//                               $("#error_desc").val("");
//                               $("#payment_expiry_date").val("");
//                               $("#search_code").val("");
//                               $("#tSx").remove();
//                               $("<i id='tSx' class='red circular exclamation triangle icon'></i>").appendTo($("#Prn").parent());
//                               $('.prnError ').html("Failed to generate PRN");
//                               console.log("failed to generate PRN");

//                         }
                        
//                   }

//                },

//                error: function(response) {
//                   console.log(response);
//                   $('.prnError').html("Invalid PRN. Try later");
                  
//                   console.log(response)
//                },

//                complete: function (response) {
                 
//                    $('#spinner').hide();
//                    $("#loading").removeClass("loading")
//                },

//          });

//       }else{
//          //licencing fees  
//          $.ajax({
//                url: application_fee_url, 
//                type: "post",
//                data: {
//                   "application_fee": application_fee,
//                   "tin": tin,
//                },
//                dataType: "json",
//                headers: {'X-CSRFToken': csrftoken },
//                mode: 'same-origin',  
//                beforeSend: function () {
                 
//                   $('#spinner').show();
//                   $("#loading").addClass("loading")
//                },
               
//                success: function (ura_response) {
//                   const response = ura_response
//                   let val = response[ Object.keys( response )[ 0 ] ]

//                   if( Object.keys( val )[ 0 ] === "GetPRNResult" ) {
                     
//                      console.log( '1',val[ 'GetPRNResult' ] )

//                      tin_response = {
//                         'status': response.GetPRNResponse.GetPRNResult.ErrorDesc,
//                         'prn': response.GetPRNResponse.GetPRNResult.PRN,
//                         'error_code': response.GetPRNResponse.GetPRNResult.ErrorCode,
//                         'error_desc': response.GetPRNResponse.GetPRNResult.ErrorDesc,
//                         'payment_expiry_date': response.GetPRNResponse.GetPRNResult.ExpiryDate,
//                         'search_code': response.GetPRNResponse.GetPRNResult.SearchCode
//                      }
//                      console.log(tin_response)

//                      if(tin_response.status === "SUCCESS"){
//                         $("#prn").val(tin_response.prn)
//                         $("#error_code").val(tin_response.error_code)
//                         $("#rror_desc").val(tin_response.error_desc)
//                         $("#payment_expiry_date").val(tin_response.payment_expiry_date)
//                         $("#search_code").val(tin_response.search_code)
//                         $('#prnError').html('');

//                      } else if (tin_response.status === "INVALID TIN") {
//                            $("#tin").val('');
//                            $('#gernerate_prn').prop('checked', false)
//                            $("#prn").val('');
//                            swal.fire(status);
//                            $('.prnError').html('');
//                      } else if(tin_response.status === "Invalid Length of TIN Entered, please try again"){
//                            swal.fire(tin_response.status);
//                            $("#prn").val("");
//                            $("#error_code").val("");
//                            $("#error_desc").val("");
//                            $("#payment_expiry_date").val("");
//                            $("#search_code").val("");
//                            // $("<i class='tSx' class='green circular check mark icon'></i>" ).appendTo($("#Prn").parent());
//                            $('.prnError').html('');
//                            console.log("invalid tin number");
//                      } else{
//                            $("#prn").val("");
//                            $("#error_code").val("");
//                            $("#error_desc").val("");
//                            $("#payment_expiry_date").val("");
//                            $("#search_code").val("");
//                            $("#tSx").remove();
//                            $("<i id='tSx' class='red circular exclamation triangle icon'></i>").appendTo($("#Prn").parent());
//                            $('.prnError ').html("Failed to generate PRN");
//                            console.log("failed to generate PRN");

//                      }
                     
//                   } 
//                   else {
//                         console.log( '2', val )
                        
//                         tin_response = {
//                            'status': val.ErrorDesc,
//                            'prn': val.PRN,
//                            'ErrorCode': val.ErrorCode,
//                            'ErrorDesc': val.ErrorDesc,
//                            'ExpiryDate': val.ExpiryDate,
//                            'SearchCode': val.SearchCode
//                         }
//                         console.log(tin_response)

//                         if(tin_response.status === "SUCCESS"){
//                            $("#prn").val(tin_response.prn)
//                            $("#error_code").val(tin_response.ErrorCode)
//                            $("#error_desc").val(tin_response.ErrorDesc)
//                            $("#payment_expiry_date").val(tin_response.ExpiryDate)
//                            $("#search_code").val(tin_response.SearchCode)
//                            $('.prnError').html('');

//                         } else if (tin_response.status === "INVALID TIN") {
//                               $("#tin").val('');
//                               $('#gernerate_prn').prop('checked', false)
//                               $("#prn").val('');
//                               swal.fire(status);
//                               $('.prnError').html('');
//                         } else if(tin_response.status === "Invalid Length of TIN Entered, please try again"){
//                               swal.fire(tin_response.status);
//                               $("#prn").val("");
//                               $("#error_code").val("");
//                               $("#error_desc").val("");
//                               $("#payment_expiry_date").val("");
//                               $("#search_code").val("");
//                               // $("<i class='tSx' class='green circular check mark icon'></i>" ).appendTo($("#Prn").parent());
//                               $('.prnError').html('');
//                               console.log("invalid tin number");
//                         } else{
//                               $("#prn").val("");
//                               $("#error_code").val("");
//                               $("#error_desc").val("");
//                               $("#payment_expiry_date").val("");
//                               $("#search_code").val("");
//                               $("#tSx").remove();
//                               $("<i id='tSx' class='red circular exclamation triangle icon'></i>").appendTo($("#Prn").parent());
//                               $('.prnError ').html("Failed to generate PRN");
//                               console.log("failed to generate PRN");

//                         }
                        
//                   }

//                },

//                error: function(response) {
//                   console.log(response);
//                   $('.prnError').html("Invalid PRN. Try later");
//                   console.log(response)
//                },

//                complete: function (response) {
                 
//                   $('#spinner').hide();
//                   $("#loading").removeClass("loading")
//                },

//          });

//       }

//    } else{
//       document.getElementById("prn").value = ''
//       document.getElementById("error_code").value = ''
//       document.getElementById("error_desc").value = ''
//       document.getElementById("payment_expiry_date").value = ''
//       document.getElementById("search_code").value = ''
//    }    

// });
   

const licence_fee_switch = document.getElementById('generate_prn_licence_fee');
licence_fee_switch.addEventListener("click",  function generatePaymentRegistrationNumberLiceneFee(e){

   const generate_prn_licence_fee  = document.getElementById('generate_prn_licence_fee').value
   
   const licence_fee_tin = document.getElementById('licence_fee_tin').value
   const licence_fee = document.getElementById("licence_fee").value
   const licence_fee_prn  = document.getElementById('licence_fee_prn').value
   const licence_fee_error_code  = document.getElementById('licence_fee_error_code').value
   const licence_fee_error_desc  = document.getElementById('licence_fee_error_desc').value
   const licence_fee_search_code  = document.getElementById('licence_fee_search_code').value
   const payment_expiry_date  = document.getElementById('payment_expiry_date').value
   
   const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
   const licence_fee_url = "{% url 'payments:get_prn_licence_fee' %}"
   
   if( tin === ''){
      Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'TIN field can not be empty',
            showConfirmButton: true,
      })

      document.getElementById("generate_prn").checked = false;

   }

   if(licence_fee_switch.checked == true){

         $.ajax({
               url: licence_fee_url , 
               type: "post",
               data: {
                  "licence_fee": licence_fee,
                  "tin": tin,
               },
               dataType: "json",
               headers: {'X-CSRFToken': csrftoken },
               mode: 'same-origin',  
               beforeSend: function () {
                  
                   $('#spinner').show();
                   $("#loading").addClass("loading")
                   
               },
               
               success: function (ura_response) {
                  
                  const response = ura_response
                  let val = response[ Object.keys( response )[ 0 ] ]

                  if( Object.keys( val )[ 0 ] === "GetPRNResult" ) {
                     
                     console.log( '1',val[ 'GetPRNResult' ] )

                     tin_response = {
                        'status': response.GetPRNResponse.GetPRNResult.ErrorDesc,
                        'licence_fee_prn': response.GetPRNResponse.GetPRNResult.PRN,
                        'licence_fee_error_code': response.GetPRNResponse.GetPRNResult.ErrorCode,
                        'licence_fee_error_desc': response.GetPRNResponse.GetPRNResult.ErrorDesc,
                        'payment_expiry_date': response.GetPRNResponse.GetPRNResult.ExpiryDate,
                        'licence_fee_search_code': response.GetPRNResponse.GetPRNResult.SearchCode
                     }
                     console.log(tin_response)

                     if(tin_response.status === "SUCCESS"){

                           $("#licence_fee_prn").val(tin_response.licence_fee_prn)
                           $("#licence_fee_error_code").val(tin_response.error_code)
                           $("#licence_fee_error_desc").val(tin_response.error_desc)
                           $("#payment_expiry_date").val(tin_response.payment_expiry_date)
                           $("#licence_fee_search_code").val(tin_response.search_code)
                           $('#prnError').html('');

               
                     } else if (tin_response.status === "INVALID TIN") {
                           
                           $("#licence_fee_tin").val('');
                           $('#generate_prn_licence_fee').prop('checked', false)
                           $("#licence_fee_prn").val('');
                           $('.prnError').html('');
                           Swal.fire({
                              icon: 'Error',
                              title: 'error',
                              text: "Invalid TIN ",
                              showConfirmButton: true,
                           })
            
                     } else if(tin_response.status === "Invalid Length of TIN Entered, please try again"){
                           
                           $("#licence_fee_prn").val('')
                           $("#licence_fee_error_code").val('')
                           $("#licence_fee_error_desc").val('')
                           $("#payment_expiry_date").val('')
                           $("#licence_fee_search_code").val('')
                           $('#prnError').html('');
                           Swal.fire({
                              icon: 'Error',
                              title: 'error',
                              text: "Invalid TIN Length",
                              showConfirmButton: true,
                           })
                     
                     } else{
                           
                           $("#licence_fee_prn").val('')
                           $("#licence_fee_error_code").val('')
                           $("#licence_fee_error_desc").val('')
                           $("#payment_expiry_date").val('')
                           $("#licence_fee_search_code").val('')
                           $('#prnError').html('');

                           $("#tSx").remove();

                           $("<i id='tSx' class='red circular exclamation triangle icon'></i>").appendTo($("#Prn").parent());
                           $('.prnError ').html("Failed to generate PRN");
                           console.log("failed to generate PRN");

                     }
                     
                  } 
                  else {
                        console.log( '2', val )
                        
                        tin_response = {
                           'status': val.ErrorDesc,
                           'prn': val.PRN,
                           'ErrorCode': val.ErrorCode,
                           'ErrorDesc': val.ErrorDesc,
                           'ExpiryDate': val.ExpiryDate,
                           'SearchCode': val.SearchCode
                        }
                        console.log(tin_response)

                        if(tin_response.status === "SUCCESS"){
                           $("#prn").val(tin_response.prn)
                           $("#error_code").val(tin_response.ErrorCode)
                           $("#error_desc").val(tin_response.ErrorDesc)
                           $("#payment_expiry_date").val(tin_response.ExpiryDate)
                           $("#search_code").val(tin_response.SearchCode)
                           $('.prnError').html('');

                        } else if (tin_response.status === "INVALID TIN") {
                              $("#tin").val('');
                              $('#gernerate_prn').prop('checked', false)
                              $("#prn").val('');
                              swal.fire(status);
                              $('.prnError').html('');
                        } else if(tin_response.status === "Invalid Length of TIN Entered, please try again"){
                              swal.fire(tin_response.status);
                              $("#prn").val("");
                              $("#error_code").val("");
                              $("#error_desc").val("");
                              $("#payment_expiry_date").val("");
                              $("#search_code").val("");
                              // $("<i class='tSx' class='green circular check mark icon'></i>" ).appendTo($("#Prn").parent());
                              $('.prnError').html('');
                              console.log("invalid tin number");
                        } else{
                              $("#prn").val("");
                              $("#error_code").val("");
                              $("#error_desc").val("");
                              $("#payment_expiry_date").val("");
                              $("#search_code").val("");
                              $("#tSx").remove();
                              $("<i id='tSx' class='red circular exclamation triangle icon'></i>").appendTo($("#Prn").parent());
                              $('.prnError ').html("Failed to generate PRN");
                              console.log("failed to generate PRN");

                        }
                        
                  }

               },

               error: function(response) {
                  $('.prnError').html("Invalid PRN. Try later");
                  console.log(response)
               },

               complete: function (response) {
                 
                   $('#spinner').hide();
                   $("#loading").removeClass("loading")
               },

         });


   } else{

      document.getElementById("licence_fee_prn").value = ''
      document.getElementById("licence_fee_error_code").value = ''
      document.getElementById("licence_fee_error_desc").value = ''
      document.getElementById("licence_fee_search_code").value = ''
      document.getElementById("payment_expiry_date").value = ''

   }    

});
