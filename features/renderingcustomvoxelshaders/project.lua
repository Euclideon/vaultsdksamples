project "RenderingCustomVoxelShaders"
	kind "ConsoleApp"
	language "C++"
	cppdialect "C++11"
	flags { "FatalWarnings" }
	tags { "vault-project" }

	targetdir "../../builds/features/renderingcustomvoxelshaders"
	debugdir "../../builds/features/renderingcustomvoxelshaders"

	--Files to include
	files { "*.h", "*.cpp", "*.md", "*.lua" }
	includedirs { "../../external/stb", "../shared" }

	--This project includes
	IncludeVaultSDK()

	-- filters
	filter { "configurations:Debug" }
		symbols "On"
		optimize "Debug"
		removeflags { "FatalWarnings" }

	filter { "configurations:Release" }
		optimize "Full"

	filter { "system:windows" }
		links { "vaultSDK" }
		postbuildcommands { 'XCOPY /f /d /y "' .. _OPTIONS["vaultsdk"] .. '\\lib\\win_x64\\vaultSDK.dll" "$(TargetDir)\\"' }

	filter { "system:linux" }
		links { "vaultSDK", "z", "m" }

		--This need to be changed to work in other distros
		postbuildcommands { 'cp "' .. _OPTIONS["vaultsdk"] .. '/lib/ubuntu18.04_GCC_x64/libvaultSDK.so" "%{cfg.targetdir}/"' }

	filter { "system:macosx" }
		frameworkdirs { "../../builds/features/renderingcustomvoxelshaders" }
		links { "vaultSDK.framework" }
		prebuildcommands { 'cp -af "../../builds/vaultsdk/lib/vaultSDK.framework" "../../builds/features/renderingcustomvoxelshaders/vaultSDK.framework"' }

	filter {}
