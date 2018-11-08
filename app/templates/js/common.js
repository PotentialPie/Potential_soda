$(function(){
	$(".login-info").hover(function(){
		$(".login-info .downlist").toggle();
	});	
	var vHeight=$(window).height()-$(".header").height()
	$(".sidebar").height($(document).height()-$(".header").height())
	$(".sidebar h2").click(function(){
		if(!$(".sidebar").is(".fold")){
			$(".sidebar").animate({width:"36px"},"fast",function(){$(".sidebar").addClass("fold")})
			$(".sidebar").find(".menu-second,.menu-third").slideUp();
			$(".sidebar .arrow-down").addClass("active");
			$("div").delegate(".sidebar.fold .menu-first > li","mouseenter",function(){
				$(this).find(".menu-second").show();
				$(this).find(".menu-third").show();
			 });
			 $("div").delegate(".sidebar.fold .menu-first > li","mouseleave",function(){
				$(this).find(".menu-second").hide();
				$(this).find(".menu-third").hide();
				//alert(2)
			 });
				
		}else{
			$(".sidebar").animate({width:"160px"},"fast",function(){$(".sidebar").removeClass("fold")});
		}
	})
	$(".sidebar .menu-first > li").mouseenter(function(){
		if($(".sidebar").is(".fold")){
			$(this).find(".menu-second").show();
			$(this).find(".menu-third").show();
		}
	})
	$(".sidebar .menu-first > li").mouseleave(function(){
		if($(".sidebar").is(".fold")){
			$(this).find(".menu-second").hide();
			$(this).find(".menu-third").hide();
		}
	})
	$(".sidebar a").not("[data-toggle=dropdown]").click(function(){
		$(".sidebar a").removeClass("active");
		$(this).parents(".menu-second").siblings().addClass("active");
		$(this).addClass("active");
	});
	$(".sidebar a.title[data-toggle=dropdown]").click(function(){
		if(!$(".sidebar").is(".fold")){
			$(this).parent().siblings().children(".menu-second,.menu-third").slideUp();
			$(this).siblings(".menu-second,.menu-third").slideToggle();
			$(this).toggleClass("active");
			$(this).parent().siblings().find("a.title").removeClass("active");			
		}
	})
	//sidebar 三级菜单（预留）
	$(".sidebar .menu-second a[data-toggle=dropdown]").click(function(){
		if(!$(".sidebar").is(".fold")){
			$(this).siblings(".menu-second,.menu-third").slideToggle()
			$(this).find(".arrow-down").toggleClass("active");
		}
	})
	$(".sidebar .menu-second a.active").parents(".menu-second").siblings("a.title").addClass("active")
	//树控件的折叠展开
	$(".tree-box").height($(window).height()-45)
	$(".tree-box .btn-toggle").click(function(){
		$(this).parent().toggleClass("fold")
	})
	//表单折叠展开
	$(".close-box .close-box-head").on("click",function(){
		$(this).toggleClass("active").siblings(".close-box-head").removeClass("active")
		$(this).next(".close-box-content").toggleClass("active").siblings(".close-box-content").removeClass("active");
	});
})