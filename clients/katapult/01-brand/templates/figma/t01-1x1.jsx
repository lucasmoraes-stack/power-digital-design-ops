const imgTemplate01FullImage = "assets/e50104b6-c7af-4728-a3ea-94cf81900d8d.png";
const imgPhotoFull = "assets/54e6576c-4638-4a17-a4b4-f7e67bf29fdd.png";
const imgLayer1 = "assets/d1808507-2acd-43b7-a695-ea2c053d4014.svg";

export default function Template01FullImage() {
  return (
    <div className="relative size-full" data-node-id="547:1043" data-name="template-01-full-image">
      <div aria-hidden className="absolute inset-0 pointer-events-none">
        <img alt="" className="absolute max-w-none object-cover size-full" src={imgTemplate01FullImage} />
        <div className="absolute bg-[rgba(0,0,0,0.25)] inset-0" />
      </div>
      <div className="absolute left-0 size-[1200px] top-0" data-node-id="547:1044" data-name="photo-full">
        <div aria-hidden className="absolute inset-0 pointer-events-none">
          <div className="absolute inset-0 overflow-hidden">
            <img alt="" className="absolute h-[136.02%] left-[-8.68%] max-w-none top-[-36%] w-[117.35%]" src={imgPhotoFull} />
          </div>
          <div className="absolute bg-gradient-to-b from-[37.218%] from-[rgba(0,0,0,0)] inset-0 to-[122.03%] to-black" />
        </div>
      </div>
      <div className="-translate-x-1/2 absolute content-stretch flex flex-col gap-[40px] items-center left-[calc(50%-0.5px)] top-[686px] w-[1101px]" data-node-id="547:1045">
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Bold'] font-bold leading-[0.9] min-w-full not-italic relative shrink-0 text-[112px] text-center text-white tracking-[-4.48px] w-[min-content]" data-node-id="547:1046">
          The upgrade your kitchen deserves.
        </p>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.2] min-w-full not-italic relative shrink-0 text-[40px] text-center text-white w-[min-content]" data-node-id="547:1047">
          No credit needed. Just fair terms and your yes.
        </p>
        <div className="bg-[#ed5370] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1048" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1048;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
      <div className="absolute content-stretch flex items-center justify-between left-[72.9px] top-[1119px] w-[1055px]" data-node-id="547:1049">
        <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[0] not-italic relative shrink-0 text-[15px] text-white w-[512px]" data-node-id="547:1050">
          <p className="leading-[1.2] mb-0">Lease-purchase service. Total cost exceeds cash price.</p>
          <p className="leading-[1.2]">Approval required. Not available in MN, NJ, WI, WY. See katapult.com.</p>
        </div>
        <div className="h-[35px] relative shrink-0 w-[157.198px]" data-node-id="547:1051" data-name="Layer_1">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLayer1} />
        </div>
      </div>
    </div>
  );
}