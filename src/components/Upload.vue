<template>
    <el-upload class="pop-upload" ref="upload" action="" :file-list="fileList" :auto-upload="false" :multiple="true"
        :on-change="handleChange" :on-remove="handleRemove">
        <template #trigger>
            <el-button type="primary">选取文件</el-button>
        </template>
        <el-button style="margin-left: 10px;" type="success" @click="submitUpload">上传到服务器</el-button>
    </el-upload>
</template>

<script>
import { ElMessage, ElLoading } from 'element-plus'
import axios from "axios"    // 此处为请求的封装方法，没有引用可以忽略
export default {
    data() {
        return {
            fileList: [],   // 定义一个空数组
        };
    },
    methods: {
        // 文件状态改变时的钩子，添加文件、上传成功和上传失败时都会被调用,function(file, fileList)
        handleChange(file, fileList) {
            this.fileList = fileList
        },
        // 删除文件之前的钩子，参数为上传的文件和文件列表，若返回 false 或者返回 Promise 且被 reject，则停止删除。function(file, fileList)
        handleRemove(file, fileList) {
            this.fileList = fileList
        },
        //上传服务器
        submitUpload() {
            //判断是否有文件再上传
            if (this.fileList.length === 0) {

                return ElMessage({
                    message: '请选取文件后再上传.',
                    type: 'warning',
                })
            }



            // 下面的代码将创建一个空的FormData对象:
            const formData = new FormData()
            // 你可以使用FormData.append来添加键/值对到表单里面；
            formData.append('audio', this.fileList[0].raw)
            formData.append('face', this.fileList[1].raw)
            formData.append('fps', 30)
            console.log(formData)
            // 添加自定义参数，不传可删除
            const loading = ElLoading.service({
                lock: true,
                text: '正在生成,请稍等......',
                background: 'rgba(0, 0, 0, 0.7)',
            })
            axios
                .post('http://172.20.10.3:8888/lip-sync', formData, {
                    responseType: "blob"
                })
                .then(response => {
                    console.log(response)
                    let blob = new Blob([response.data], { type: 'video/mp4' });
                    let downloadElement = document.createElement("a");
                    let href = window.URL.createObjectURL(blob); //创建下载的链接
                    downloadElement.href = href;
                    downloadElement.download = "result.mp4"; //下载后文件名
                    document.body.appendChild(downloadElement);
                    downloadElement.click(); //点击下载
                    document.body.removeChild(downloadElement); //下载完成移除元素
                    window.URL.revokeObjectURL(href); //释放掉blob对象
                    loading.close()
                })
                .catch(function (error) { // 请求失败处理
                    console.log(error);
                    loading.close()
                });

        },
    },
};
</script>