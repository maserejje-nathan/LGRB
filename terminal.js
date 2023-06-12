 formData = {
               
     purpose_of_application : purpose_of_application,
     previous_licence_number : previous_licence_number,
     name_of_the_company : name_of_the_company,
     company_status : company_status,
     licence_type : licence_type,
     tin : tin,
     plot_number : plot_number,
     projected_gross_turnover : projected_gross_turnover,
     description : description,
     class_of_the_casino_games : class_of_the_casino_games,
     categories_of_machines : categories_of_machines,
     engagement_capacity : engagement_capacity,
     start_date : start_date,
     end_date : end_date,
     previous_business_engagement : previous_business_engagement,
     name_of_the_employer : name_of_the_employer,
     crime_engagement : crime_engagement,
     crime_details : crime_details,
             
     tenancy_agreement : tenancy_agreement,
     memorandum_and_articles_of_association : memorandum_and_articles_of_association,
     annual_company_returns : annual_company_returns,
     districts_of_conduction : districts_of_conduction,
     application_fee : application_fee,
     licence_fee : licence_fee,
     prn : prn,
     email : email,
     form_confirmation : form_confirmation,

     ura_district : ura_district,
     ura_county : ura_county,
     ura_subcounty : ura_subcounty,
     ura_village : ura_village,
    
 }
 
 $.ajax({
    type: 'post',
    url: '{% url "new:principle-apply" %}',
    headers: {'X-CSRFToken': csrftoken },
    data: licenceData,
    // dataType: 'json',
    // contentType: 'application/json',
    contentType: false, 
    processData: false, 

    success: function(response) {
       if (response.success) {
          
          Swal.fire({
             icon: 'success',
             title: 'Success',
             text: response.message,
             showConfirmButton: true,
          })

          $('#modal-form-licence-fee').hide();
          // Perform any additional actions or updates on the page
       } else {
          console.log('Error: ' + response.errors);
       }
    },

    error: function(xhr, textStatus, errorThrown) {
       console.log('Error: ' + errorThrown);
    }


 });