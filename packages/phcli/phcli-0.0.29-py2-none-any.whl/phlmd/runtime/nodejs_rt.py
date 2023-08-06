from phlmd.runtime.lambda_rt import LambdaRuntime


class NodejsRT(LambdaRuntime):
    __runtime_name = "nodejs"

    def pkg_layer(self, data):
        """
        组织 layer 的打包逻辑
        :param data
            :arg lib_path: 指定 nodejs 的 lib 位置
            :arg package_name: 打包的名称
        """

        self._package_cmds = [
            "mkdir -p %s/%s/node_modules" % (self._package_root, self.__runtime_name),
            "cp -r %s/* %s/%s/node_modules/" % (data["lib_path"], self._package_root, self.__runtime_name),
            "cd %s && zip -r -q ../package.zip . && cd -" % self._package_root,
            "rm -rf %s" % self._package_root,
        ]

        self.package(data["package_name"])

    def pkg_code(self, data):
        """
        组织 code 的打包逻辑
        :param data
            :arg name: 项目名称
            :arg code_path: 需要打包的代码位置
            :arg package_name: 打包的名称
        """

        self._package_cmds = [
            "mkdir -p %s/%s" % (self._package_root, self.__runtime_name),
            "npm run build",
        ]

        for cmd in data["code_path"].split(","):
            if cmd.endswith("/"):
                cmd = cmd[:-1]
            self._package_cmds.append("cp -r %s %s/%s/" % (cmd, self._package_root, self.__runtime_name))

        if "name" in data.keys():
            self._package_cmds.extend([
                f"mv {self._package_root}/{self.__runtime_name}/config/project/{data['name']}.yml {self._package_root}/{self.__runtime_name}/config/server.yml",
                f"rm -rf {self._package_root}/{self.__runtime_name}/config/project/"
            ])

        self._package_cmds.extend([
            "cd %s/%s && zip -r -q ../../package.zip . && cd -" % (self._package_root, self.__runtime_name),
            "rm -rf %s" % self._package_root,
        ])

        self.package(data["package_name"])
