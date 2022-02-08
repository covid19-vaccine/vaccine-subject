/**
 * MedDRA API JS: Add listener for AEs inlines, monitor ae selected from medDRA
 * dictionary, get selected term code and call medDRA detail endpoint to query
 * for further details on the AE term and finally populate related fields on the
 * form i.e llt code and name, hlt code and name ... etc.
 * **/
$(document).ready(function () {
	(function($) {
		var form_id = 'id_adverseeventrecord_set-TOTAL_FORMS';
		var total_formset = document.getElementById('total-formset').textContent;
		var error_message = '';
	
		if (total_formset && total_formset > 0) {
			for (count = 0; count < total_formset; count++) {
				addListener(count);
			}
		}
	
	    $(document).on('formset:added', function(event, $row, formsetName) {
	    	let form_count = document.getElementById(form_id).value - 1;
	        addListener(form_count);
	    });
			
	    function addListener(index) {
	    	let select_id = 'id_adverseeventrecord_set-'+index+'-search_code';
			let select_field = document.getElementById(select_id);
			$(document).on('change', '#'+select_id, function() {
				// Reset values already selected before doing a looking for selected code.
				resetRelatedFields(index);

				setLoading(true);
				selected = select_field.value;
				// Perform search on medDRA dict, when option selected.
				if (selected) {
					updateDetails(selected, index);
				} else {
					setLoading(false);
				}
			});
	    }
	    
	    async function updateDetails(selected = '', index=0) {
	    	let url = '/edc_meddra/meddra/detail/' + selected;
	    	try {
	    		let response = await fetch(url);
	        	if (response.status === 200) {
	        		let data = await response.json();
	        		let details = data['mds'][0];
	        		
	        		// Update corresponding MedDRA fields.
	        		updateRelatedFields(index, details);

	        		// Toggle error message and loading (remove).
	        		toggleErrorMessage(error_message, index);
	        		setLoading(false);
	        		return;
	        	}

	        	// Toggle error message and loading (add and display to user).
	        	toggleErrorMessage('Testing', index);
	        	setLoading(false);

	    	} catch (err) {
	    		setLoading(false);
	    		console.error(err);
	    	}
	    }
	    
	    function setLoading(loading=false) {
	    	let loader = document.getElementById('loader');
	    	if (loading) {
	    		loader.classList.remove('hide-loader');
	    	} else {
	    		loader.classList.add('hide-loader');
	    	}
	    	
	    }

	    function updateRelatedFields(index, details) {
    		// Low level term name and code for selected code.
    		let lltcode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-llt_code');
    		lltcode_field.value = details['lltcode'];
    		let lltname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-llt_name');
    		lltname_field.value = details['lltname'];
    		// Preferred term name and code for selected code.
    		let ptcode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-pt_code');
    		ptcode_field.value = details['ptcode'];
    		let ptname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-pt_name');
    		ptname_field.value = details['ptname'];
    		// High level term name and code for selected code.
    		let hltcode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-hlt_code');
    		hltcode_field.value = details['hltcode'];
    		let hltname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-hlt_name');
    		hltname_field.value = details['hltname'];
    		// High level group term name and code for selected code.
    		let hlgtcode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-hlgt_code');
    		hlgtcode_field.value = details['hlgtcode'];
    		let hlgtname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-hlgt_name');
    		hlgtname_field.value = details['hlgtname'];
    		// System organ class name and code for selected code.
    		let soccode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-soc_code');
    		soccode_field.value = details['soccode'];
    		let socname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-soc_name');
    		socname_field.value = details['socname'];
	    }

	    function resetRelatedFields(index) {
	    	// Low level term name and code for selected code.
    		let lltcode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-llt_code');
    		lltcode_field.value = '';
    		let lltname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-llt_name');
    		lltname_field.value = '';
    		// Preferred term name and code for selected code.
    		let ptcode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-pt_code');
    		ptcode_field.value = '';
    		let ptname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-pt_name');
    		ptname_field.value = '';
    		// High level term name and code for selected code.
    		let hltcode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-hlt_code');
    		hltcode_field.value = '';
    		let hltname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-hlt_name');
    		hltname_field.value = '';
    		// High level group term name and code for selected code.
    		let hlgtcode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-hlgt_code');
    		hlgtcode_field.value = '';
    		let hlgtname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-hlgt_name');
    		hlgtname_field.value = '';
    		// System organ class name and code for selected code.
    		let soccode_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-soc_code');
    		soccode_field.value = '';
    		let socname_field = document.getElementById(
    				'id_adverseeventrecord_set-'+index+'-soc_name');
    		socname_field.value = '';
	    }
	    
	    function toggleErrorMessage(message='', index) {

	    	// If no error message, remove if already existing.
	    	let field_class = document.getElementsByClassName('field-search_code')[index];
	    	field_class.classList.remove('errors');
    		let errorlist_elem = document.getElementsByClassName('errorlist')[0];

    		if (errorlist_elem) {
    			field_class.removeChild(errorlist_elem);
    		}
	    	
	    	if (message) {
	    		// Add a 'ul' element for the error list, and append message.
	    		field_class.classList.add('errors');
	    	    
		    	let errorlist_elem = document.createElement("ul");
		    	errorlist_elem.classList.add('errorlist');
		    	
		    	let error_node = document.createElement("li");
		    	let error_text = document.createTextNode(message);

		    	error_node.appendChild(error_text);

		    	errorlist_elem.appendChild(error_node);
		    	field_class.appendChild(errorlist_elem);
	    	}
	    }
	
	})(django.jQuery);
});